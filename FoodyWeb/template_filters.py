from FoodyWeb import web
from FoodyCore.extensions import ServerRedis


@web.app_template_filter(name="ServerRedis")
def ServerRedis(name=None):
    """
    This is a wrapper for Redis server Query object in template
    """
    if not name:
        return False
    return ServerRedis.get(name=name)


print("[OK] Template Filters checked. <FoodyWeb>".capitalize())
