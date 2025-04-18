from flask import request


def wants_json() -> bool:
    return (
        request.path.endswith(".json")
        or request.accept_mimetypes["application/json"]
        > request.accept_mimetypes["text/html"]
    )
