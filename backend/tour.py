from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from config import config

import jwt
import datetime
import hashlib


tour = Blueprint("tour", __name__)

client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel

# 투어 카드 다 받아오기
# @tour.route("/", methods=["GET"])
# def getTours():
#     tour_list = list(db.card.find({}))
#     for tour in tour_list:
#         tour["_id"] = str(tour["_id"])
#     return jsonify({"tour_list": tour_list})


# 투어 카드 생성
@tour.route("/", methods=["POST"])
def createTour():
    tour_url = request.form["tour_url"]
    tour_title = request.form["tour_title"]
    tour_location = request.form["tour_location"]
    tour_continent = request.form["tour_continent"]
    tour_date = request.form["tour_date"]
    tour_content = request.form["tour_content"]

    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"msg": "로그인을 해주세요"}
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    doc = {
        "url": tour_url,
        "title": tour_title,
        "location": tour_location,
        "continent": tour_continent,
        "date": tour_date,
        "content": tour_content,
        "like": 0,
        "author_id": payload["user_id"],
    }

    db.card.insert_one(doc)
    return jsonify({"msg": "추가완료"})


# 투어 카드 id로 받아오기
@tour.route("/<tour_id>", methods=["GET"])
def getTour(tour_id):
    query = {"_id": ObjectId(tour_id)}
    tour = db.card.find_one(query)

    if tour:
        tour["_id"] = str(tour["_id"])
        return tour

    return jsonify({"tour": tour})


# # 투어 카드 user_id로 받아오기
# @tour.route("/mytour", methods=["GET"])
# def getTourByUser():
#     token_receive = request.cookies.get("mytoken")
#     if token_receive is None:
#         return {"msg": "로그인을 해주세요"}
#     payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

#     tour_list = list(db.card.find({"author_id": payload["user_id"]}))

#     for tour in tour_list:
#         tour["_id"] = str(tour["_id"])
#     return jsonify({"tour_list": tour_list})


# 투어 카드 대륙별로 받아오기
@tour.route("/continent", methods=["POST"])
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

    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"msg": "권한이 없습니다"}
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
        return jsonify({"msg": "수정완료"})
    else:
        return jsonify({"msg": "수정 권한이 없습니다."})


# 카드 삭제하기
@tour.route("/<tour_id>", methods=["DELETE"])
def deleteTour(tour_id):
    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"msg": "권한이 없습니다"}
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    selected_card = db.card.find_one({"_id": ObjectId(tour_id)})

    if payload["user_id"] == selected_card["author_id"]:
        db.card.delete_one({"_id": ObjectId(tour_id)})
    else:
        return jsonify({"msg": "수정 권한이 없습니다."})

    return jsonify({"msg": "삭제완료"})
