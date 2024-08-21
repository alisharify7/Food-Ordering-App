"""
 * Food Ordering Application
 * ssr applications url pattern
 * author: github.com/alisharify7
 * email: alisharifyofficial@gmail.com
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

# ssr url
from Auth import auth
from Web import web
from Admin import admin
from User import user


urlpatterns = [
    {"prefix": "/", "obj": web},
    {"prefix": "/user/", "obj": user},
    {"prefix": "/auth/", "obj": auth},
    {"prefix": "/admin/", "obj": admin},
]
