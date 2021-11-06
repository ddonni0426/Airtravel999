from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from pymongo import MongoClient
from bson import ObjectId
from config import config
import os
from os.path import join, dirname, realpath

UPLOADS_PATH = join(dirname(realpath(__file__)), 'static\\images')

import jwt
import datetime
import hashlib


tour = Blueprint("tour", __name__)

client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel

# 투어 카드 다 받아오기
@tour.route("/", methods=["GET"])
def getTours():
    tour_list = list(db.card.find({}))
    for tour in tour_list:
        tour["_id"] = str(tour["_id"])
    return jsonify({"tour_list": tour_list})


# 투어 카드 생성
@tour.route("/", methods=["POST"], strict_slashes=False)
def createTour():
    tour_url = request.files['file']
    print('@@@@', tour_url)
    tour_url.save(os.path.join(UPLOADS_PATH, secure_filename(tour_url.filename)))
    tour_title = request.form["tour_title"]
    tour_location = request.form["tour_location"]
    tour_continent = request.form["tour_continent"]
    tour_date = request.form["tour_date"]
    tour_content = request.form["tour_content"]

    if tour_url is None: 
        return jsonify({"result": "fail url", "msg": "이미지를 첨부해주세요"})
    if tour_title is None:
        return jsonify({"result": "fail title", "msg": "제목을 입력해주세요"})
    if len(tour_title) > 15:
        return jsonify({"result": "fail title", "msg": "제목은 15자 이하로 적어주세요"})
    if tour_location is None:
        return jsonify({"result": "fail location", "msg": "위치를 입력해주세요"})
    if tour_continent is None:
        return jsonify({"result": "fail continent", "msg": "대륙을 선택해주세요"})
    if tour_date is None:
        return jsonify({"result": "fail date", "msg": "날짜를 선택해주세요"})
    if tour_content is None:
        return jsonify({"result": "fail content", "msg": "내용을 입력해주세요"})
        

    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"result": "fail", "msg": "로그인을 먼저 해주세요"}
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    doc = {
        "url": secure_filename(tour_url.filename),
        "title": tour_title,
        "location": tour_location,
        "continent": tour_continent,
        "date": tour_date,
        "content": tour_content,
        "like": 0,
        "author_id": payload["user_id"],
        "nick": payload["nick"],
    }
    db.card.insert_one(doc)
    return jsonify({"result":"success", "msg": "추가완 료"})


# 투어 카드 id로 받아오기
@tour.route("/<tour_id>", methods=["GET"])
def getTour(tour_id):
    query = {"_id": ObjectId(tour_id)}
    tour = db.card.find_one(query)

    if tour:
        tour["_id"] = str(tour["_id"])
        return tour

    return jsonify({"result":"success", "tour": tour})


# # 투어 카드 user_id로 받아오기
# @tour.route("/mytour", methods=["GET"])
# def getTourByUser():
#     token_receive = request.cookies.get("mytoken")
#     if token_receive is None:
#         return {"msg": "로그인을 해주세 요"}
#     payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

#     tour_list = list(db.card.find({"author_id": payload["user_id"]}))

#     for tour in tour_list:
#         tour["_id"] = str(tour["_id"])
#     return jsonify({"tour_list": tour_list})


# 투어 카드 대륙별로 받아오기
@tour.route("/continent", methods=["POST"], strict_slashes=False)
def filterByContinent():
    continent = request.form["continent"]    
    if continent == "Continent":
        tour_list = list(db.card.find({}))
    else:
        tour_list = list(db.card.find({"continent": continent}))
    for tour in tour_list:
        tour["_id"] = str(tour["_id"])
    return jsonify({"tour_list": tour_list})


# 투어 카드 수정하기
@tour.route("/<tour_id>", methods=["PUT"])
def updateTour(tour_id):
    tour_url = request.form["tour_url"]
    tour_title = request.form["tour_title"]
    tour_location = request.form["tour_location"]
    tour_continent = request.form["tour_continent"]
    tour_date = request.form["tour_date"]
    tour_content = request.form["tour_content"]

    if tour_url is None: 
        return jsonify({"result": "fail url", "msg": "이미지를 첨부해주세요"})
    if tour_title is None:
        return jsonify({"result": "fail title", "msg": "제목을 입력해주세요"})
    if len(tour_title) > 15:
        return jsonify({"result": "fail title", "msg": "제목은 15자 이하로 적어주세요"})
    if tour_location is None:
        return jsonify({"result": "fail location", "msg": "위치를 입력해주세요"})
    if tour_continent is None:
        return jsonify({"result": "fail continent", "msg": "대륙을 선택해주세요"})
    if tour_date is None:
        return jsonify({"result": "fail date", "msg": "날짜를 선택해주세요"})
    if tour_content is None:
        return jsonify({"result": "fail content", "msg": "내용을 입력해주세요"})

    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return jsonify({"result": "fail", "msg": "권한이 없습니다"})

    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    selected_card = db.card.find_one({"_id": ObjectId(tour_id)})

    if payload["user_id"] == selected_card["author_id"]:
        doc = {
            "url": tour_url,
            "title": tour_title,
            "location": tour_location,
            "continent": tour_continent,
            "date": tour_date,
            "content": tour_content,
            "like": 0,
        }
        db.card.update_one({"_id": ObjectId(tour_id)}, {"$set": doc})
        return jsonify({"result": "success", "msg": "수정완료"})
    else:
        return jsonify({"result": "fail", "msg": "수정 권한이 없습니다"})


# 카드 삭제하기
@tour.route("/<tour_id>", methods=["DELETE"])
def deleteTour(tour_id):
    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return jsonify({"result": "fail", "msg": "권한이 없습니다"})
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    selected_card = db.card.find_one({"_id": ObjectId(tour_id)})

    if payload["user_id"] == selected_card["author_id"]:
        db.card.delete_one({"_id": ObjectId(tour_id)})
    else:
        return jsonify({"result": "fail", "msg": "수정 권한이 없습니다"})

    return jsonify({"result":"success", "msg": "삭제완료"})