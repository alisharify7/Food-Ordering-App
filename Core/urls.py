from Auth import auth
from Order import order
from Web import web
from Admin import admin


urlpatterns = [
    {"prefix": "", "obj": web},
    {"prefix": "/auth/", "obj": auth},
    {"prefix": "/admin/", "obj": admin},
    {"prefix": "/order/", "obj": order},
]