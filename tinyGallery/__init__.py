import os
import time
from . import db, auth, image, remark, user, homepage
from flask import *
from markupsafe import escape

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        secret_key = b'905bd5453270081b623caf48b2c59159b25121018a1bddeda190f9c4fa77e2a4',
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "database.sqlite"),
        CONFIG_FILE = os.path.join(app.instance_path, "config.json")
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # set up the database
    db.init_app(app)

    # user admin module
    app.register_blueprint(auth.bp)

    # image admin module
    app.register_blueprint(image.imagebp)

    # remarks admin module
    app.register_blueprint(remark.remarkbp)

    # user admin module
    app.register_blueprint(user.userbp)

    # homepage
    app.register_blueprint(homepage.homepagebp)

    return app
