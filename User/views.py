from User import user
from flask import render_template
from flask_login import login_required


@user.route("", methods=["GET"])
@login_required
def index_get():
    return render_template("user/index.html")


