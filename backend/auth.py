from flask import Blueprint, request, jsonify
from pymongo import MongoClient

auth = Blueprint("auth", __name__)

client = MongoClient('localhost', 27017)
db = client.airtravel

SECRET_KEY = "AirTravel_AweSome_Team"

import jwt
import datetime
import hashlib

@auth.route('/')
def getTour():
  return "auth"

# 회원가입 API
@auth.route("/register", methods=["POST"])
def api_register():
    id = request.form["id"]
    pw = request.form["pw"]
    nickname = request.form["nickname"]

    pw_hash = hashlib.sha256(pw.encode("utf-8")).hexdigest()

    db.user.insert_one({"id": id, "pw": pw_hash, "nick": nickname})

    return jsonify({"result": "success"})
	
# 로그인 API
@auth.route('/login', methods=['POST'])
def api_login():
    id = request.form['id']
    pw = request.form['pw']

    pw_hash = hashlib.sha256(pw.encode('utf-8')).hexdigest()

    result = db.user.find_one({'id': id, 'pw': pw_hash})

    if result is not None:
        payload = {
            'id': id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=3)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '회원정보 오류입니다.'})
