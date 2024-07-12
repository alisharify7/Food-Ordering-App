from flask import Blueprint



admin = Blueprint(
    name="admin",
    import_name=__name__,
    static_folder="static/admin",
    template_folder="templates/admin"
)

import Admin.views

