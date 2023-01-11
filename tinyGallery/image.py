import time
import json
import uuid
import os
import shutil
import cv2
import functools
from flask import *
from werkzeug.utils import secure_filename
from tinyGallery.db import get_db

ALLOWED_EXTENSIONS =  {"jpg", "png" ,"webp", "bmp", "jpeg"}
UPLOAD_FOLDER = os.path.join("tinyGallery", "static", "posts")

imagebp = Blueprint("image", __name__, url_prefix="/image")

def allowed_file(filename):
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@imagebp.route("/upload", methods=("GET", "POST"))
def upload_file():

    # Infomations from client
    user_name = session.get("user_id")
    title = request.form["postTitle"]
    description = request.form["description"]
    # Type: String, value: "on" or "None"
    status_of_auto_select_cover = str(request.form.get("StatusOfAutoSelectCover"))

    # Files
    files = request.files.getlist("uploadFiles")
    cover_file = None

    # Infomations from server
    cover_file_type = ""
    date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    post_uuid = str(uuid.uuid4())
    current_post_dir = os.path.join(UPLOAD_FOLDER, post_uuid)
    orginal_size_images_path = os.path.join(UPLOAD_FOLDER, "orginalSizeImages", post_uuid)

    if request.method != "POST":
        flash("method error")
        return "This page is post only", 500
    elif not user_name:
        flash("User not logged in")
        return "You are not logged in", 500
    elif status_of_auto_select_cover == "None":
        cover_file = request.files["postCoverImage"]
        if cover_file.filename == "":
            flash("No selected cover file")
            return "No selected cover file", 500
    elif not files[0].filename:
        flash("No selected file")
        return "No selected file", 500
    elif title == "" or title == None:
        flash("Title not be none")
        return "Title not be none", 500

    file_names = []
    files_type = []

    # Judging the number of files and set post_type
    if files.__len__() > 1:
        post_type = "multipleImg"
        for f in files:
            current_file_name = secure_filename(f.filename)
            file_names.append(current_file_name)

            current_file_type = current_file_name.split('.')[-1]
            files_type.append(current_file_type)
    # If number of files is one then file_names and files_type length is 1
    else:
        post_type = "singleImg"
        file_names.append(secure_filename(files[0].filename))
        files_type.append(secure_filename(files[0].filename).split('.')[-1])


    # create path
    os.makedirs(current_post_dir)
    os.makedirs(orginal_size_images_path)

    db = get_db()

    def resize_images(image_name):
        original_image = cv2.imread(os.path.join(orginal_size_images_path, image_name))
        h, w = original_image.shape[:2]
        new_h, new_w = int(h / 3), int(w / 3)
        image_resize = cv2.resize(original_image, (new_w,new_h))
        # if name of image file equal to current post uuid,
        # then it will be the current post cover
        if image_name == post_uuid:
            cv2.imwrite(os.path.join(current_post_dir, image_name + ".jpg"), image_resize)
        else:
            cv2.imwrite(os.path.join(current_post_dir, image_name), image_resize)
    
    # if user only uploads a single image, this will serve as the cover,
    # upload multiple image, the cover is first uploaded image in it.
    # The cover image file name is post uuid.
    if post_type == "multipleImg":
        for x in file_names:
            if not allowed_file(str(x)):
                flash("Not allowed file type")
                return "Not allowed file type", 500
        
        loop = 0
        for x in files:
            x.save(os.path.join(orginal_size_images_path, secure_filename(x.filename) ))
            if loop == 0:
                if status_of_auto_select_cover == "on":
                    cover_file_type = x.filename.split('.')[-1]
                    try:
                        shutil.copy2(os.path.join(orginal_size_images_path, secure_filename(x.filename)),
                        os.path.join(orginal_size_images_path, post_uuid + "." + cover_file_type)
                        )
                    except IOError:
                        return "Failed to upload files.", 500
                    resize_images(post_uuid + "." + cover_file_type)
                elif status_of_auto_select_cover == "None":
                    cover_file = request.files["postCoverImage"]
                    cover_file_type = secure_filename(cover_file.filename).split('.')[-1]
                    cover_file.save(os.path.join(orginal_size_images_path, post_uuid + "." + cover_file_type) )
                    resize_images(post_uuid + "." + cover_file_type)
                    

            loop = loop + 1

        for x in file_names:
            resize_images(x)


    elif post_type == "singleImg":
        if not allowed_file(file_names[0]):
            flash("Not allowed file type")
            return "Not allowed file type", 500
        
        files[0].save(os.path.join(orginal_size_images_path, file_names[0]))


        if status_of_auto_select_cover == "on":
            cover_file_type = file_names[0].split('.')[-1]
            try:
                shutil.copy2(os.path.join(orginal_size_images_path, file_names[0]),
                os.path.join(orginal_size_images_path, post_uuid + "." + cover_file_type)
                )
            except IOError:
                flash("Failed to copy cover file")
                return "Failed to upload files.", 500
            resize_images(post_uuid + "." + cover_file_type)
        elif status_of_auto_select_cover == "None":
            cover_file = request.files["postCoverImage"]
            cover_file_type = secure_filename(cover_file.filename).split('.')[-1]
            cover_file.save(os.path.join(orginal_size_images_path, post_uuid + "." + cover_file_type) )
            resize_images(post_uuid + "." + cover_file_type)


        resize_images(file_names[0])

    
    try:
        db.execute(
            """INSERT INTO posts(postFilePath, type, coverFileType, postTitle, description, nsfw, userName, date, postUUID)
            VALUES (?,?,?,?,?,?,?,?,?)""",
            (current_post_dir, post_type, cover_file_type, title, description, 0, user_name, date, post_uuid),
        )
        db.commit()
    except db.IntegrityError:
        return "failed to post image", 500
    
    return redirect(url_for("/.index_page"))


# @imagebp.route("/getimagesJSON", methods=("GET", "POST"))
# def get_images():

#     if request.method == "POST":
#         db = get_db()

#         try:
#             image_table = db.execute(
#                 "SELECT * FROM images;"
#             ).fetchall()
#         except db.IntegrityError:
#             return "Failed to get images"

#         testDict = {}
#         objects_list = []
#         for row in image_table:
#             d = testDict
#             d['id'] = row[0]
#             d['fileName'] = row[1]
#             d['imageTitle'] = row[2]
#             d['description'] = row[3]
#             d['dots'] = row[4]
#             d['user'] = row[5]
#             d['date'] = row[6]
#             d['uuid'] = row[7]
#             objects_list.append(d)
        
#         imagesJson = json.dumps(objects_list,ensure_ascii=False)
#         return imagesJson
#     else:
#         return "This page is post only"

@imagebp.route("/likedThisPOST")
def liked_this_post():
    post_uuid = request.args.get("UUID")
    liked_status = request.args.get("likedStatus")
    user_name = session.get("user_id")

    if not user_name:
        return "You are not logged in", 400
    
    db = get_db()

    if liked_status == "like":
        # Get the row for duplicate check
        data_for_duplicate_check = db.execute(
            "SELECT * FROM likedPost WHERE userName = ? AND postUUID = ?",
            (user_name, post_uuid),
        ).fetchone()

        error = None

        if data_for_duplicate_check:

            if data_for_duplicate_check["likeStatus"] == 1:
                error = "You can't liked a post more than once"
                return error, 400

            try:
                db.execute(
                    "UPDATE likedPost SET likeStatus = 1 WHERE userName = ? AND postUUID = ?",
                    (user_name, post_uuid),
                )
                db.commit()
            except db.IntegrityError:
                error = "Failed to connect database"
        else:
            # If user like this post, its status is 1. contrary unlike status is 0
            try:
                db.execute(
                    "INSERT INTO likedPost(userName, postUUID, likeStatus) VALUES (?,?,?)",
                    (user_name, post_uuid, 1),
                )
                db.commit()
            except db.IntegrityError:
                error = "Failed to connect database"

        try:
            before_dots = db.execute(
                "SELECT dots, postUUID FROM posts WHERE postUUID = ?",
                (post_uuid,),
            ).fetchone()
        except db.IntegrityError:
            error = "Failed to connect database"

        current_dots = before_dots["dots"] + 1

        try:
            db.execute(
                "UPDATE posts SET dots = ? WHERE postUUID = ?",
                (current_dots, post_uuid),
            )
            db.commit()
        except db.IntegrityError:
            error = "Failed to connect database"

        if error == None:
            return jsonify(
                status = "like",
                dots = current_dots
            )
        else:
            return error, 400
    
    if liked_status == "unlike":
        error = None

        try:
            data_for_duplicate_check = db.execute(
                "SELECT * FROM likedPost WHERE userName = ? AND postUUID = ?",
                (user_name, post_uuid),
            ).fetchone()
        except db.IntegrityError:
            error = "Failed to connect database"
        
        if not data_for_duplicate_check:
            error = "You haven't unliked any post"
            return error, 400

        if data_for_duplicate_check["likeStatus"] == 0:
            error = "You can't unliked a post more than once"
            return error, 400

        try:
            db.execute(
                "UPDATE likedPost SET likeStatus = 0 WHERE userName = ? AND postUUID = ?",
                (user_name, post_uuid),
            )
            db.commit()
        except db.IntegrityError:
            error = "Failed to connect database"

        try:
            before_dots = db.execute(
                "SELECT dots, postUUID FROM posts WHERE postUUID = ?",
                (post_uuid,),
            ).fetchone()
        except db.IntegrityError:
            error = "Failed to connect database"

        current_dots = before_dots["dots"] - 1

        try:
            db.execute(
                "UPDATE posts SET dots = ? WHERE postUUID = ?",
                (current_dots, post_uuid),
            )
            db.commit()
        except db.IntegrityError:
            error = "Failed to connect database"

        if error == None: 
            return jsonify(
                status = "unlike",
                dots = current_dots
            )
        else:
            return error, 400