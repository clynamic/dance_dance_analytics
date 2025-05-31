from flask import request


def get_request_data():
    data = request.get_json(silent=True)
    if data and isinstance(data, dict):
        return data
    return request.form
