from flask import request


def get_single_query_arg(param_name: str) -> str | None:
    values = request.args.getlist(param_name)
    return values[0] if len(values) == 1 else None
