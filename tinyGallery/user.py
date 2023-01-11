import os
import functools
import cv2
from flask import *
from tinyGallery.db import get_db
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS =  {"jpg", "png" ,"webp", "gif"}
UPLOAD_FOLDER = os.path.join("tinyGallery", "static", "avatars", "originalSize")

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

userbp = Blueprint("user", __name__, url_prefix="/user")

@userbp.route("userProfile/<user_id>", methods=("GET", "POST"))
def user_profile(user_id):
    db = get_db()

    try:
        user_posts = db.execute(
            "SELECT * FROM posts WHERE userName = ?;", (user_id,)
        ).fetchall()
    except db.IntegrityError:
        return "Failed to get your posts"

    return render_template("profile.html", user_name = user_id, user_posts = user_posts)

@userbp.route("setUpProfile", methods=("GET", "POST"))
def set_up_user_profile():
    if request.method == "POST": 

        avatar_image = request.files["userAvatar"]
        user_id = session.get("user_id")
        fileType = avatar_image.filename.split('.')[-1]


        if avatar_image.filename == "":
            flash("No selected file")
            return "No selected file"
        if avatar_image and allowed_file(avatar_image.filename):
            avatar_image.save(os.path.join(UPLOAD_FOLDER, user_id + ".png"))

            # resize image
            image_for_opencv = cv2.imread(os.path.join(UPLOAD_FOLDER, user_id + ".png"))
            resize_image = cv2.resize(image_for_opencv, (200,200))
            cv2.imwrite(os.path.join("tinyGallery", "static", "avatars", user_id + ".jpg"), resize_image)

            return redirect(url_for("user.user_profile", user_id = user_id))
    else:
        return "This page is post only"