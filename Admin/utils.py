import uuid
from FoodyAdmin.model import Admin


def LoadAdminObject(admin_id : int) -> Admin:
    """ Load Admin via admin primary key """
    return Admin.query.get(admin_id) or None


def LoadAdminObjectPublickKey(public_key : uuid) -> Admin:
    """ Load admin via admin Public key """
    return Admin.query.filter_by(PublicKey=public_key).first() or None

