from flask import Flask, render_template, request
from pymongo import MongoClient
from config import config
import jwt
import datetime
import hashlib

from like import like
from auth import auth
from tour import tour

client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel

app = Flask(__name__)
app.register_blueprint(tour, url_prefix="/tour")
app.register_blueprint(like, url_prefix="/like")
app.register_blueprint(auth, url_prefix="/auth")


@app.route("/")
def home():
    user_token = request.cookies.get("mytoken")
    user_nickname = ""
    if user_token is not None:
        payload = jwt.decode(user_token, config["SECRET_KEY"], algorithms=["HS256"])
        user_info = db.user.find_one({"user_id": payload["user_id"]}, {"_id": False})
        user_nickname = user_info["nick"]
    else:
        user_nickname = None
    tour_list = list(db.card.find({}))
    for tour in tour_list:
        tour["_id"] = str(tour["_id"])
    return render_template("index.html", lists=tour_list, userNickName=user_nickname)


if __name__ == "__main__":
    app.run("0.0.0.0", port=5050, debug=True)
