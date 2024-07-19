"""
 * celery main app starter
 * author: @alisharify7
 * Copyleft 2023-2024. under GPL-3.0 license
 * https://github.com/alisharify7/Food-Ordering-App
"""

from FoodyCore import create_app

flask_app = create_app()
celery_app = flask_app.extensions["celery"]

