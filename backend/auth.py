from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from config import config
import jwt
import datetime
import hashlib

auth = Blueprint("auth", __name__)

client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel

# 아이디 중복확인 체크 API
@auth.route("/checkid", methods=["POST"])
def api_checkid():
    user_id = request.form["user_id"]
		
    result = db.user.find_one({"user_id": user_id})

    if result is not None:
      return jsonify({"result": "success", "msg": "아이디가 이미 사용중입니다."})
    else:
      return jsonify({"result": "success", "msg": "사용가능한 아이디입니다."})

# 회원가입 API
@auth.route("/signup", methods=["POST"])
def api_register():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    nickname = request.form["nickname"]

    result = db.user.find_one({"user_id": user_id})

    if result is not None:
      return jsonify({"result": "fail", "msg": "아이디가 이미 사용중입니다."})
    else:
      pw_hash = hashlib.sha256(user_pw.encode("utf-8")).hexdigest()

      db.user.insert_one({"user_id": user_id, "user_pw": pw_hash, "nick": nickname})

      return jsonify({"result": "success"})
	
# 로그인 API
@auth.route('/login', methods=['POST'])
def api_login():
    user_id = request.form['user_id']
    user_pw = request.form['user_pw']

    pw_hash = hashlib.sha256(user_pw.encode('utf-8')).hexdigest()

    result = db.user.find_one({'user_id': user_id, 'user_pw': pw_hash})

    if result is not None:
        payload = {
            'user_id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60*60*60)
        }
        token = jwt.encode(payload, config["SECRET_KEY"], algorithm='HS256')

        return jsonify({'result': 'success', 'token': token})
    else:
        return jsonify({'result': 'fail', 'msg': '회원정보 오류입니다.'})

# 유저정보 확인 API
@auth.route('/user', methods=['GET'])
def api_valid():
    token_receive = request.cookies.get('mytoken')

    try:
        payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=['HS256'])

        userinfo = db.user.find_one({'user_id': payload['user_id']}, {'_id': 0})
        return jsonify({'result': 'success', 'nickname': userinfo['nick']})
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'fail', 'msg': '로그인 시간이 만료되었습니다.'})
    except jwt.exceptions.DecodeError:
        return jsonify({'result': 'fail', 'msg': '로그인 정보가 존재하지 않습니다.'})
