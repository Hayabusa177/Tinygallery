import time
import json
import os
import uuid
import glob
import functools
from flask import *
from tinyGallery.db import get_db

remarkbp = Blueprint("remark", __name__, url_prefix="/remark")

@remarkbp.route("imageDetailPage/<post_uuid>", methods=("GET", "POST"))
def image_detail_page(post_uuid):
    
    user_name = session.get("user_id")

    if post_uuid == "" or post_uuid == None:
        return "Image not found"
    
    db = get_db()
    try:
        user_data = db.execute(
            "SELECT description, userName, date, dots, type, coverFileType FROM posts WHERE postUUID = ?;", (post_uuid,)
        ).fetchone()

        remarks = db.execute(
            "SELECT * FROM remarks WHERE postUUID = ? ORDER BY date DESC;", (post_uuid,)
        ).fetchall()

        liked_data = db.execute(
            """SELECT postUUID FROM likedPost
            WHERE postUUID = ?
            AND userName = ?
            AND likeStatus = 1;""",
            (post_uuid, user_name,)
        ).fetchone()

    except db.IntegrityError:
        return "Failed to get datas"

    files_name_list = []
    if user_data["type"] == "multipleImg":
        paths_list = glob.glob(os.path.join("tinyGallery", "static", "posts", "orginalSizeImages", post_uuid, "*"))
        for x in paths_list:
            c = os.path.split(x)
            files_name_list.append(c[-1])
        files_name_list.sort()
        del files_name_list[-1]
        print(files_name_list)

    return render_template("imageDetailPage.html",user_name = user_name,
    post_uuid = post_uuid, 
    datas = user_data, 
    files_name_list = files_name_list,
    remarks = remarks,
    liked_post_uuid= liked_data)
        


@remarkbp.route("sendRemark", methods=("GET", "POST"))
def send_remark():

    if request.method == "POST":
        user_name = session.get("user_id")
        
        if user_name != None or user_name != "":
            db = get_db()

            post_uuid = request.form["UUID"]
            remark_uuid = str(uuid.uuid4())
            remark_content = request.form["remarkContent"]
            reply_to = request.form["replyTo"]
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if remark_content == "" or remark_content == None:
                return "Remarks content can not be none"

            try:
                db.execute(
                    "INSERT INTO remarks(postUUID, userName, content, replyTo, date, remarkUUID) VALUES (?,?,?,?,?,?)",
                    (post_uuid, user_name, remark_content, reply_to, date, remark_uuid),
                )
                db.commit()
                return redirect(url_for("remark.image_detail_page", post_uuid = post_uuid))

            except db.IntegrityError:
                return "Failed to send remark"
        else:
            return "You are not logged in"
    else:
        return "This page is post only"

