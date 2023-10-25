from flask import Blueprint, session
from FoodyAdmin.utils import LoadAdminObject



admin = Blueprint(
    name="admin",
    import_name=__name__,
    static_folder="static",
    template_folder="templates"
)

import FoodyAdmin.views
import FoodyAdmin.model

@admin.app_context_processor
def admin_context():
    funcs = {
        "GetAdmin": LoadAdminObject(admin_id=session.get("account-id", ""))
    }
    return funcs


# apps:
import FoodyAdmin.api
import FoodyAdmin.Apps.Setting.views
import FoodyAdmin.Apps.ManageUsers.views
import FoodyAdmin.Apps.ManageFoods.views
import FoodyAdmin.Apps.Accounting.views
import FoodyAdmin.Apps.ManageSMS.views