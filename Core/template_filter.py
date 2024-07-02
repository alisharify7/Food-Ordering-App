from flask import current_app, url_for

def StorageUrl(path: str):
    """This template filter generate dynamic urls base of app.debug mode for serving statics via flask or nginx in production or development
        if debug mode is on this filter redirect users to flask.serve function
        but in production mode this filter redirect users to serve static via nginx
    """
    if path[0] == "/":
        path = path[1:]

    if current_app.debug:
        return url_for("ServeStorageFiles", path=path, _external=True)  # flask serve
    else:
        return f"/Storage/{path}"  # Nginx Serve Files


templatesFilters = {
    "StorageUrl": StorageUrl
}

def contexts():
    ctx = {}
    return ctx
