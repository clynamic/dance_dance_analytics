from flask import request, redirect


def strip_empty_query_params():
    if request.method == "GET" and request.args:
        new_args = {k: v for k, v in request.args.items() if v.strip() != ""}
        if len(new_args) < len(request.args):
            cleaned_query = "&".join(f"{k}={v}" for k, v in new_args.items())
            return redirect(
                f"{request.path}{'?' + cleaned_query if cleaned_query else ''}"
            )
    return None
