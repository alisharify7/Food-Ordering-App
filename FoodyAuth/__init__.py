from flask import Blueprint


auth = Blueprint(
    name="auth",
    import_name=__name__,
    static_folder="static/auth",
    template_folder="templates"
)


import FoodyAuth.views
import FoodyAuth.model