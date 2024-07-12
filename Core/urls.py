from Auth import auth
from Order import order
from Web import web
from Admin import admin
from User import user


urlpatterns = [
    {"prefix": "", "obj": web},
    {"prefix": "/user/", "obj": user},
    {"prefix": "/auth/", "obj": auth},
    {"prefix": "/admin/", "obj": admin},
    {"prefix": "/order/", "obj": order},
]
