from Admin import admin
from flask import render_template
from Auth.AccessControl import admin_login_required





@admin.route("/", methods=["GET"])
@admin_login_required
def index_get():
    return render_template("index.html")


