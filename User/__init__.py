from flask import Blueprint


user = Blueprint(
    name='user',
    import_name=__name__,
    static_folder='static',
    template_folder='templates'
)


import User.views