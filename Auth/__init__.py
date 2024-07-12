from flask import Blueprint

auth = Blueprint(
    name="auth",
    import_name=__name__,
    static_folder="static/auth",
    template_folder="templates/auth",
    static_url_path="AuthStorage"
)

import Auth.views
import Auth.model
