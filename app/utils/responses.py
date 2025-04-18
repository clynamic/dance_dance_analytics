from flask import jsonify


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
