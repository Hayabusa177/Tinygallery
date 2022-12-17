import time
import json
import os
import functools
from flask import *
from tinyGallery.db import get_db

remarkbp = Blueprint("remark", __name__, url_prefix="/remark")

@remarkbp.route("imageDetailPage/<post_uuid>", methods=("GET", "POST"))
def image_detail_page(post_uuid):

    if post_uuid != "":
        db = get_db()
        try:
            user_data = db.execute(
                "SELECT description, user, date, dots, fileType FROM images WHERE uuid = ?;", (post_uuid,)
            ).fetchone()

            remarks = db.execute(
                "SELECT * FROM remarks WHERE postUUID = ?;", (post_uuid,)
            ).fetchall()

        except db.IntegrityError:
            return "Failed to get images"

        return render_template("imageDetailPage.html",user_name = session.get("user_id"),
        image_uuid = post_uuid, datas = user_data, remarks = remarks)
    else:
        return "Image not found"


@remarkbp.route("sendRemark", methods=("GET", "POST"))
def send_remark():

    if request.method == "POST":
        user_name = session.get("user_id")
        
        if user_name != None or user_name != "":
            db = get_db()

            uuid = request.form["UUID"]
            remark_content = request.form["remarkContent"]
            reply_to = request.form["replyTo"]
            date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

            if remark_content == "" or remark_content == None:
                return "Remarks content can not be none"

            try:
                db.execute(
                    "INSERT INTO remarks(postUUID, userName, content, replyTo, date) VALUES (?,?,?,?,?)",
                    (uuid, user_name, remark_content, reply_to, date),
                )
                db.commit()
                return redirect(url_for("remark.image_detail_page", post_uuid = uuid))

            except db.IntegrityError:
                return "Failed to send remark"
        else:
            return "You are not logged in"
    else:
        return "This page is post only"

