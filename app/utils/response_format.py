from flask import request, jsonify, render_template

from app.utils.content_route import get_request_format


def respond(payload, template=None, status=200):
    is_json = get_request_format() == "json" or request.is_json
    if is_json or not template:
        return jsonify(payload), status
    return render_template(template, **payload), status
