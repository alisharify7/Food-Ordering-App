# ssr url
from Auth import auth
from Web import web
from Admin import admin
from User import user


urlpatterns = [
    {"prefix": "", "obj": web},
    {"prefix": "/user/", "obj": user},
    {"prefix": "/auth/", "obj": auth},
    {"prefix": "/admin/", "obj": admin},
]
