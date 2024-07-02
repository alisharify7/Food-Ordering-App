from FoodyCore import app
from flask import render_template
from flask_wtf.csrf import CSRFError

errors = {
    "401": "صفحه‌ای که می‌خواهید به آن دسترسی پیدا کنید، تا زمانی که با شناسه کاربری و رمز عبور معتبر وارد سیستم شوید برای شما نمایش داده نمی‌شود. (Unauthorized) ",
    "404": "صفحه مورد نظر یافت نشد! (Not Found) ",
    "500": "خطایی سمت سرور رخ داده است، بعدا امتحان کنید (Internal Server Error) ",
    "csrf_error": "برخی مفادیر امنیتی به نظر گم شده اند یا به درستی وارد نشده اند . (Csrf Token is Missing or invalid)".title(),
    "503": "سرویس به طور موقت قادر به پاسخ گویی به شما نمی باشد. لطفا لحطاتی دیگر دوباره سعی کنید (Service Unavailable)",
}


@app.errorhandler(CSRFError)
def error_CSRFError(e):
    ctx = {
        "error": "403",
        "error_description": errors["csrf_error"]
    }
    return render_template("errors/BaseError.html", ctx=ctx), 403


# 4xx Errors
@app.errorhandler(401)
def error_401(e):
    ctx = {
        "error": 401,
        "error_description": errors["401"]
    }
    return render_template("errors/BaseError.html", ctx=ctx), 401


@app.errorhandler(404)
def error_404(e):
    ctx = {
        "error": 404,
        "error_description": errors["404"]
    }
    return render_template("errors/BaseError.html", ctx=ctx), 404


# 5xx Errors
@app.errorhandler(500)
def error_500(e):
    ctx = {
        "error": 500,
        "error_description": errors["500"]
    }
    return render_template("errors/BaseError.html", ctx=ctx), 500


@app.errorhandler(503)
def error_503(e):
    ctx = {
        "error": 503,
        "error_description": errors["500"]
    }
    return render_template("errors/BaseError.html", ctx=ctx), 500
