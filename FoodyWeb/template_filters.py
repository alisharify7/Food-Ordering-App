from FoodyWeb import web
from FoodyCore.extension import ServerRedis


@web.app_template_filter(name="ServerRedis")
def ServerRedis(name=None):
    """
    This is a wrapper for Redis server Query object in template
    """
    if not name:
        return False
    return ServerRedis.get(name=name)


print("[OK] All Template Filters checked By Flask App <FoodyWeb>".title())
