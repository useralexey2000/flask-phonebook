import os
from flask import Flask
import sys

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = 'dev',
    )

    if test_config is None:
        app.config.from_pyfile('settings.py', silent=False)
    else:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import db
    db.mongo.init_app(app)
    db.init_db(app)
    
    from . import pbook
    app.register_blueprint(pbook.bp)

    app.add_url_rule('/', endpoint='index')

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port="8080")


