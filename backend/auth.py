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

    if user_id :
        result = db.user.find_one({"user_id": user_id})

        if result is not None:
            return jsonify({"result": "fail", "msg": "아이디가 이미 사용중입니다."})
        else:
            return jsonify({"result": "success", "msg": "사용가능한 아이디입니다."})
    else: 
        return jsonify({"result": "fail", "msg": "아이디를 입력해주세요"})


# 회원가입 API
@auth.route("/signup", methods=["POST"])
def api_register():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]
    user_pwc = request.form["user_pwc"]
    user_nick = request.form["user_nick"]

    if user_id and user_pw and user_pwc and user_nick:

        if user_pw != user_pwc:
            return jsonify({"result": "fail pw", "msg": "비밀번호가 서로 일치하지 않습니다"})

        result = db.user.find_one({"user_id": user_id})

        if result :
            return jsonify({"result": "fail id", "msg": "아이디가 이미 사용중입니다"})
        else:
            pw_hash = hashlib.sha256(user_pw.encode("utf-8")).hexdigest()

            db.user.insert_one({"user_id": user_id, "user_pw": pw_hash, "nick": user_nick})

            return jsonify({"result": "success", "msg": "회원가입에 성공하였습니다"})
    else:
        return jsonify({"result": "fail"})



# 로그인 API
@auth.route("/login", methods=["POST"])
def api_login():
    user_id = request.form["user_id"]
    user_pw = request.form["user_pw"]

    if user_id is None:
        return jsonify({"result": "fail id", "msg": "아이디를 입력하세요"})
    elif user_pw is None:
        return jsonify({"result": "fail pw", "msg": "비밀번호를 입력하세요"})
    elif user_id and user_pw :
        pw_hash = hashlib.sha256(user_pw.encode("utf-8")).hexdigest()

        result = db.user.find_one({"user_id": user_id, "user_pw": pw_hash})

        if result is not None:
            payload = {
                "user_id": user_id,
                "exp": datetime.datetime.utcnow()
                + datetime.timedelta(seconds=60 * 60 * 60),
                "nick": result.get("nick")
            }
            token = jwt.encode(payload, config["SECRET_KEY"], algorithm="HS256")

            return jsonify({"result": "success", "token": token})
        else:
            return jsonify({"result": "fail check", "msg": "회원정보가 없습니다."})


# 유저정보 확인 API
@auth.route("/user", methods=["GET"])
def api_valid():
    token_receive = request.cookies.get("mytoken")

    try:
        payload = jwt.decode(token_receive, config["SECRET_KEY"], algorithms=["HS256"])

        userinfo = db.user.find_one({"user_id": payload["user_id"]}, {"_id": 0})
        return jsonify({"result": "success", "nickname": userinfo["nick"]})
    except jwt.ExpiredSignatureError:
        return jsonify({"result": "fail", "msg": "로그인 시간이 만료되었습니다."})
    except jwt.exceptions.DecodeError:
        return jsonify({"result": "fail", "msg": "로그인 정보가 존재하지 않습니다."})