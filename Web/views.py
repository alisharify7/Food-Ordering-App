from Web import web
from flask import render_template, abort, request


@web.route("/")
def index_view():
    """
    Just redirect user to login page
    You can replace this with a nice and simple landing page for you company
        return render_template('path/to/landing page.html')
    """
    return render_template("index.html")

@web.route("/page-not-found/")
def PageNotFound():
    """
        return Page Not found 404 Error
    """
    abort(404)
