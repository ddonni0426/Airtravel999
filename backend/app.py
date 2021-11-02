from pymongo import MongoClient

from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='../frontend/src')

client = MongoClient('localhost', 27017)
db = client.airtravel
doc = {
	"file": 'url',
	"location": 'Seoul',
	"continent": 'Asia',
	"date": '21-11-02',
	"content": 'fun and interesting'
}
db.card.insert_one(doc)

@app.route('/')
def home():
	return render_template('index.html')

if __name__ == '__main__':
	app.run('0.0.0.0',port=5050,debug=True)
