from flask import Blueprint, request, jsonify
from pymongo import MongoClient

auth = Blueprint("auth", __name__)

client = MongoClient('localhost', 27017)
db = client.airtravel

# SECRET_KEY = "AirTravel_AweSome_Team"

# import jwt
# import datetime
import hashlib

@auth.route('/')
def getTour():
  return "auth"


@auth.route("/register", methods=["POST"])
def api_register():
    id = request.form["id"]
    pw = request.form["pw"]
    nickname = request.form["nickname"]

    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

    db.user.insert_one({"id": id, "pw": pw_hash, "nick": nickname})

    return jsonify({"result": "success"})