from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId
from config import config
import jwt

like = Blueprint("like", __name__)
client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel


@like.route("/<tour_id>", methods=["POST"])
def likeTour(tour_id):
    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"msg": "로그인을 해주세요"}
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    tour = db.card.find_one({"_id": ObjectId(tour_id)})
    like_count = tour.get("like")

    if tour:
        db.card.update_one(
            {"_id": ObjectId(tour_id)}, {"$set": {"like": like_count + 1}}
        )
        db.like.insert_one(
            {"user_id": payload["user_id"], "card_id": ObjectId(tour_id)}
        )

    return jsonify({"msg": "좋아요 완료"})


@like.route("/<tour_id>", methods=["DELETE"])
def dislikeTour(tour_id):
    token_receive = request.cookies.get("mytoken")
    if token_receive is None:
        return {"msg": "로그인을 해주세요"}
    payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

    tour = db.card.find_one({"_id": ObjectId(tour_id)})
    like_count = tour.get("like")

    if tour:
        db.card.update_one(
            {"_id": ObjectId(tour_id)}, {"$set": {"like": like_count - 1}}
        )
        db.like.delete_one(
            {"user_id": payload["user_id"], "card_id": ObjectId(tour_id)}
        )

    return jsonify({"msg": "좋아요 취소 완료"})
