from flask import Blueprint

order = Blueprint(
    name="order",
    import_name=__name__,
    static_folder="static/order",
    template_folder="templates/order",
    static_url_path="OrderStatic"
)

# import FoodyOrder.views
import Order.model
