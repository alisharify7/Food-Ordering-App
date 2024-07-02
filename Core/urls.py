from Auth import auth
from Order import order

urlpatterns = [
    {"prefix": "/auth/", "obj": auth},
    {"prefix": "/order/", "obj": order},
]