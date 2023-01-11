import os
import time
from . import db
from flask import *
from markupsafe import escape

homepagebp = Blueprint("/", __name__, url_prefix="/")

@homepagebp.route("/")
def index_page():
    page = request.args.get("page")
    user_name = session.get("user_id")

    # Set how many post cards per page
    NUM_ELEMENT_ON_ONE_PAGE = 10
    stop_num = 0

    # Compute the stop row from sql
    if page:
        x = int(page) - 1
        stop_num = x * NUM_ELEMENT_ON_ONE_PAGE

    if not user_name:
        database = db.get_db()
        try:
            posts_table = database.execute(
                "SELECT * FROM posts ORDER BY date DESC LIMIT ? OFFSET ?;",
                (NUM_ELEMENT_ON_ONE_PAGE, stop_num),
            ).fetchall()

            number_images = database.execute(
                "SELECT id FROM posts ORDER BY id DESC;"
            ).fetchone()
            
            if posts_table:
                # Compute the page count sum
                number_of_divide = number_images[0] // NUM_ELEMENT_ON_ONE_PAGE
            else:
                number_of_divide = 0

        except database.IntegrityError:
            return "Failed to get images", 400   

        
        return render_template("index.html", 
        user_name = user_name,
        posts_data = posts_table, divide_by = number_of_divide)

    try:
        database = db.get_db()
        posts_table = database.execute(
            """SELECT * FROM posts 
            ORDER BY date DESC
            LIMIT ? OFFSET ?""",
            (NUM_ELEMENT_ON_ONE_PAGE, stop_num),
        ).fetchall()

        number_images = database.execute(
            "SELECT id FROM posts ORDER BY id DESC;"
        ).fetchone()

        liked_data = database.execute(
            "SELECT postUUID FROM likedPost WHERE userName = ? AND likeStatus = 1;",
            (user_name,)
        ).fetchall()

    except database.IntegrityError:
        return "Failed to get images", 400

    if posts_table:
        # Compute the page count sum
        number_of_divide = number_images[0] // NUM_ELEMENT_ON_ONE_PAGE
    else:
        number_of_divide = 0

    user_liked_posts_list = []
    for x in liked_data:
        user_liked_posts_list.append(str(x[0]))

    return render_template("index.html", 
    user_name = user_name,
    posts_data = posts_table, 
    liked_data = user_liked_posts_list,
    divide_by = number_of_divide)



@homepagebp.route("/test")
def test():
    return "hh"