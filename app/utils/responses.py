from flask import jsonify


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
