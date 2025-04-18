from flask_wtf.csrf import generate_csrf


def init_csrf_cookie(app):
    @app.after_request
    def set_csrf_cookie(response):
        response.set_cookie(
            "csrf_token",
            generate_csrf(),
            secure=not app.debug,
            samesite="Lax",
            httponly=False,
        )
        return response
