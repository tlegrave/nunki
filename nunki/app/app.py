import os

from flask import Flask

from . import router


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY", "9OLWxND4o83j4K4iuopO")

    app.register_blueprint(router.posts.posts)

    return app


def run_app():
    app = create_app()
    app.run()
