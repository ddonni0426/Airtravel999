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
@auth.route("/signup", methods=["POST"])
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
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*60)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '회원정보 오류입니다.'})

# 유저정보 확인 API
@auth.route('/user', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        print(payload)

        userinfo = db.user.find_one({'id': payload['id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
