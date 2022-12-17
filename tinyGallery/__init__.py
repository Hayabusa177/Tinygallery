import os
import time
from . import db, auth, image, remark, user
from flask import *
from markupsafe import escape

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        secret_key = b'905bd5453270081b623caf48b2c59159b25121018a1bddeda190f9c4fa77e2a4',
        SECRET_KEY = "dev",
        DATABASE = os.path.join(app.instance_path, "database.sqlite")
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
    @app.route("/")
    def index_page():
        page = request.args.get("page")

        NUM_ELEMENT_ON_ONE_PAGE = 8
        stop_num = 0

        if page:
            x = int(page) - 1
            stop_num = x * NUM_ELEMENT_ON_ONE_PAGE
    
        database = db.get_db()
        try:
            image_table = database.execute(
                "SELECT * FROM images LIMIT ? OFFSET ?;",
                (NUM_ELEMENT_ON_ONE_PAGE, stop_num,),
            ).fetchall()

            number_images = database.execute(
                "SELECT id FROM images ORDER BY id DESC;"
            ).fetchone()

        except database.IntegrityError:
            return "Failed to get images"

        if image_table:
            number_of_divide = number_images[0] // 8

            return render_template("index.html", 
            user_name = session.get("user_id"),
            images = image_table, divide_by = number_of_divide)

        return render_template("index.html", 
        user_name = session.get("user_id"),
        images = image_table, divide_by = 0)

    return app