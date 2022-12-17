import time
import json
import uuid
import os
import cv2
import functools
from flask import *
from werkzeug.utils import secure_filename
from tinyGallery.db import get_db

ALLOWED_EXTENSIONS =  {"jpg", "png" ,"webp", "gif"}
UPLOAD_FOLDER = os.path.join("tinyGallery", "static", "images")

imagebp = Blueprint("image", __name__, url_prefix="/image")

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@imagebp.route("/upload", methods=("GET", "POST"))
def upload_image():
    if request.method == "POST":
        title = request.form["postTitle"]
        description = request.form["description"]
        file = request.files["uploadImage"]

        fileName = secure_filename(file.filename)
        userName = session.get("user_id")
        date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        postUUID = str(uuid.uuid4())
        fileType = file.filename.split('.')[-1]
        filePath = "static/images/" + postUUID + "." + fileType

        db = get_db()

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            flash("No selected file")
            return redirect(url_for('index_page'))
        if file and allowed_file(file.filename):
            try:
                db.execute(
                    "INSERT INTO images(fileName, fileType, filePath, imageTitle, description, user, date, uuid) VALUES (?,?,?,?,?,?,?,?)",
                    (fileName, fileType, filePath, title, description, userName, date, postUUID),
                )
                db.commit()

                file.save(os.path.join(UPLOAD_FOLDER, "originalSize", postUUID + "." + fileType))
                # resize image
                image_original = cv2.imread(os.path.join(UPLOAD_FOLDER, "originalSize", postUUID + "." + fileType))
                h, w = image_original.shape[:2]
                new_h, new_w = int(h / 3), int(w / 3)
                image_resize = cv2.resize(image_original, (new_w,new_h))
                cv2.imwrite(os.path.join(UPLOAD_FOLDER, postUUID + "." + fileType), image_resize)

                return redirect(url_for("index_page"))
            except db.IntegrityError:
                return "failed to post image"

@imagebp.route("/getimagesJSON", methods=("GET", "POST"))
def get_images():

    if request.method == "POST":
        db = get_db()

        try:
            image_table = db.execute(
                "SELECT * FROM images;"
            ).fetchall()
        except db.IntegrityError:
            return "Failed to get images"

        testDict = {}
        objects_list = []
        for row in image_table:
            d = testDict
            d['id'] = row[0]
            d['fileName'] = row[1]
            d['imageTitle'] = row[2]
            d['description'] = row[3]
            d['dots'] = row[4]
            d['user'] = row[5]
            d['date'] = row[6]
            d['uuid'] = row[7]
            objects_list.append(d)
        
        imagesJson = json.dumps(objects_list,ensure_ascii=False)
        return imagesJson
    else:
        return "This page is post only"

