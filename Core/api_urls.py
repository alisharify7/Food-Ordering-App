# csr url
from Order import food_blp, order_blp

urlpatterns = [
    {"prefix": "/order/", "obj": order_blp},
    {"prefix": "/foods/", "obj": food_blp},
]
