from functools import wraps
from flask import Blueprint, request
from typing import Callable
from flask.typing import ResponseReturnValue


def content_route(
    bp: Blueprint, rule: str, **options
) -> Callable[[Callable[..., ResponseReturnValue]], Callable[..., ResponseReturnValue]]:
    def decorator(
        f: Callable[..., ResponseReturnValue],
    ) -> Callable[..., ResponseReturnValue]:
        options.setdefault("strict_slashes", False)
        base = rule.rstrip("/") or "/"

        @wraps(f)
        def wrapper(*args, **kwargs):
            format_value = kwargs.pop("format", None)
            setattr(request, "format", format_value)
            return f(*args, **kwargs)

        bp.add_url_rule(base, defaults={"format": None}, view_func=wrapper, **options)

        if base == "/":
            bp.add_url_rule(".<format>", view_func=wrapper, **options)
        else:
            bp.add_url_rule(base + ".<format>", view_func=wrapper, **options)

        return wrapper

    return decorator


def get_request_format() -> str | None:
    return getattr(request, "format", None)


def request_is_json() -> bool:
    return get_request_format() == "json"
