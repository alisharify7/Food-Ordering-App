import os
from Core import app
from flask import send_from_directory, current_app


if current_app.debug:
    @app.get("/Storage/<path:path>/")
    def ServeStorageFiles(path: os.path):
        """ This view only serve files for development only!!"""
        return send_from_directory(current_app.config.get("STORAGE_DIR"), path)
