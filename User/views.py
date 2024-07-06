from User import user
from flask import render_template



@user.route("", methods=["GET"])
def index():
    return render_template("user/base.html")


