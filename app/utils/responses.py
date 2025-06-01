from flask import jsonify, render_template
from functools import wraps
from flask import Blueprint, request
from typing import Callable
from flask.typing import ResponseReturnValue


def model_route(
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


def request_is_json() -> bool:
    if getattr(request, "format", None) == "json":
        return True

    best = request.accept_mimetypes.best_match(["application/json", "text/html"])
    if (
        best == "application/json"
        and request.accept_mimetypes[best] > request.accept_mimetypes["text/html"]
    ):
        return True

    return False


def respond(payload, template=None, status=200):
    is_json = request_is_json()
    if is_json or not template:
        return jsonify(payload), status
    return render_template(template, **payload), status


def json_data(data, status: int = 200):
    if hasattr(data, "to_dict") and callable(data.to_dict):
        data = data.to_dict()
    elif isinstance(data, list):
        data = [
            (
                item.to_dict()
                if hasattr(item, "to_dict") and callable(item.to_dict)
                else item
            )
            for item in data
        ]
    return jsonify(data), status


def json_success(message: str, data=None, status: int = 200):
    return (
        jsonify({"status": "success", "message": message, "data": data or {}}),
        status,
    )


def json_error(message: str, errors=None, status: int = 400):
    return (
        jsonify({"status": "error", "message": message, "errors": errors or {}}),
        status,
    )
