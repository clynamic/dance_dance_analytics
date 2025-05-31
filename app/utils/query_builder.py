from sqlalchemy import or_, and_
from datetime import datetime, date


def parse_value(value, field_type, is_end=False):
    if field_type == "date":
        for fmt in ("%Y-%m-%d", "%Y-%m", "%Y"):
            try:
                parsed = datetime.strptime(value, fmt)
                if fmt == "%Y":
                    return (
                        date(parsed.year, 12, 31) if is_end else date(parsed.year, 1, 1)
                    )
                elif fmt == "%Y-%m":
                    last_day = (
                        31
                        if parsed.month == 12
                        else (
                            date(parsed.year, parsed.month + 1, 1) - date.resolution
                        ).day
                    )
                    return (
                        date(parsed.year, parsed.month, last_day)
                        if is_end
                        else date(parsed.year, parsed.month, 1)
                    )
                return parsed.date()
            except ValueError:
                continue
        raise ValueError(f"Invalid date format: {value}")
    elif field_type == "int":
        return int(value)
    return value


def build_dynamic_query(base_query, args, fields):
    for param, (field_type, columns) in fields.items():
        if not isinstance(columns, list):
            columns = [columns]

        if field_type == "text":
            terms = args.getlist(f"{param}[]")
            single = args.get(param)
            if single:
                terms.append(single)
            if terms:
                filters = []
                for term in terms:
                    term_filters = [col.ilike(f"%{term.strip()}%") for col in columns]
                    filters.append(or_(*term_filters))
                if filters:
                    base_query = base_query.filter(or_(*filters))

        elif field_type == "id":
            terms = args.getlist(f"{param}[]")
            single = args.get(param)
            if single:
                terms.append(single)
            if terms:
                filters = []
                for term in terms:
                    term_filters = []
                    for col in columns:
                        try:
                            converted = col.type.python_type(term)
                            term_filters.append(col == converted)
                        except (ValueError, AttributeError):
                            continue
                    if term_filters:
                        filters.append(or_(*term_filters))
                if filters:
                    base_query = base_query.filter(or_(*filters))

        elif field_type in ("date", "int"):
            values = args.getlist(param)
            if not values:
                value = args.get(param)
                if value:
                    values = [value]
            expressions = []
            for part in values:
                part = part.strip()
                if "..." in part:
                    start, end = part.split("...")
                    start_val = parse_value(start, field_type, is_end=False)
                    end_val = parse_value(end, field_type, is_end=True)
                    exprs = [and_(col >= start_val, col < end_val) for col in columns]
                    expressions.append(or_(*exprs))
                elif ".." in part:
                    start, end = part.split("..")
                    start_val = parse_value(start, field_type, is_end=False)
                    end_val = parse_value(end, field_type, is_end=True)
                    exprs = [and_(col >= start_val, col <= end_val) for col in columns]
                    expressions.append(or_(*exprs))
                elif part.startswith(">="):
                    val = parse_value(part[2:], field_type)
                    exprs = [col >= val for col in columns]
                    expressions.append(or_(*exprs))
                elif part.startswith(">"):
                    val = parse_value(part[1:], field_type)
                    exprs = [col > val for col in columns]
                    expressions.append(or_(*exprs))
                elif part.startswith("<="):
                    val = parse_value(part[2:], field_type)
                    exprs = [col <= val for col in columns]
                    expressions.append(or_(*exprs))
                elif part.startswith("<"):
                    val = parse_value(part[1:], field_type)
                    exprs = [col < val for col in columns]
                    expressions.append(or_(*exprs))
                else:
                    val = parse_value(part, field_type)
                    exprs = [col == val for col in columns]
                    expressions.append(or_(*exprs))
            if expressions:
                base_query = base_query.filter(or_(*expressions))
    return base_query
