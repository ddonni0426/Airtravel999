from flask import Flask, render_template
from pymongo import MongoClient
from config import config

from like import like
from auth import auth
from tour import tour

client = MongoClient(config["DB_URL"], 27017)
db = client.airtravel

app = Flask(__name__)
app.register_blueprint(tour, url_prefix="/tour")
app.register_blueprint(like, url_prefix="/like")
app.register_blueprint(auth, url_prefix="/auth")


@app.route('/')
def home():
    tour_list = list(db.card.find({}))
    for tour in tour_list:
        tour['_id'] = str(tour['_id'])
    return render_template('index.html', lists=tour_list)

if __name__ == '__main__':
	app.run('0.0.0.0',port=5050,debug=True)
