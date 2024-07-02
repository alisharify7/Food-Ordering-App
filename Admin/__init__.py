from flask import Blueprint



admin = Blueprint(
    name="admin",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

import Admin.model

