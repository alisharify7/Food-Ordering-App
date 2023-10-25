from flask import Blueprint

order = Blueprint(
    name="order",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

import FoodyOrder.views
import FoodyOrder.model
