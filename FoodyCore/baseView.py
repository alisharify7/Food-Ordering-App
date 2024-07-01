import uuid

from flask import session, request, url_for
from FoodyConfig.config import STATUS
from FoodyCore import app
import FoodyAuth.utils as AuthUtils



@app.before_request
def before_request():
    """
    This Middleware like django authentication put some data in request before heads up to actual view
    :return: None

        is_userAuthenticated = True  : if user is authenticated
        is_userAuthenticated = False  : if user is not authenticated


        user_object = Sqlalchemy<User Object>  : if is_userAuthenticated is True
        user_object = None  : if is_userAuthenticated is False

    """
    request.is_userAuthenticated = False
    request.user_object = None

    if (account_id := session.get("account-id")):
        user_db = AuthUtils.LoadUserObject(account_id)
        if user_db:
            request.is_userAuthenticated = True if session.get("login") else False
            request.user_object = user_db




@app.context_processor
def app_context():
    """Global App Content Processor"""
    from FoodyAdmin.model import SiteSetting
    from FoodyConfig.config import DOMAIN



    def get_app_info() -> dict:
        """
            this template filter return app info like name domain and ...
        """
        site = SiteSetting.query.filter(SiteSetting.tag == "setting").first()
        return {
            "name": site.Name,
            "description": site.Description,
            "domain": DOMAIN,
            "address": site.Address,
            "phone": site.Phone,
        }

    def check_app_logo() -> bool:
        """
            this template filter check app logo is set or not
        """
        site = SiteSetting.query.filter(SiteSetting.tag == "setting").firts()
        return True if site.Logo else False

    def generate_uuid() -> str:
        """
        use this function for generating uuid in templates
        uses for id or class attribute in html
        """
        return str(uuid.uuid4()).replace(" ", "").replace("-", "")


    def serve_app_logo() -> str:
        """
        this view serve app logo
        if there is no image 
         return default logo image
        """
        if (site := SiteSetting.query.filter_by(tag="setting").first()):
            if site.Logo:
                if not STATUS:
                    return (f'/Media/{site.Logo}')  # nginx serve
                else:
                    return url_for("web.Serve", path=(site.Logo))

        if not STATUS:
            return ("/Media/logo.png")  # nginx serve
        else:
            return url_for("web.Serve", path=("logo.png"))

    return {
        "get_app_info": get_app_info,
        "check_app_logo": check_app_logo,
        "serve_app_logo": serve_app_logo,
        "uuid4": generate_uuid,
        "getuser": AuthUtils.LoadUserObject,
    }
