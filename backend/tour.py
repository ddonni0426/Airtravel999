from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

tour = Blueprint('tour', __name__)

client = MongoClient('localhost', 27017)
db = client.airtravel

# 투어 카드 다 받아오기
@tour.route('/', methods=['GET'])
def getTours():
  tour_list = list(db.card.find({}))
  for tour in tour_list:
            tour['_id'] = str(tour['_id'])
  return jsonify({'tour_list': tour_list})

# 투어 카드 생성
@tour.route('/', methods=['POST'])
def createTour():
  tour_url = request.form['tour_url']
  tour_title = request.form['tour_title']
  tour_location = request.form['tour_location']
  tour_continent = request.form['tour_continent']
  tour_date = request.form['tour_date']
  tour_content = request.form['tour_content']
  doc = {
    "url": tour_url,
    "title": tour_title,
    "location": tour_location,
    "continent": tour_continent,
    "date": tour_date,
    "content": tour_content,
    "like": False
  }

  db.card.insert_one(doc)
  return jsonify({'msg': '추가완료'})

# 투어 카드 id로 받아오기
@tour.route('/<tour_id>', methods=['GET'])
def getTour(tour_id):
  query= {'_id': ObjectId(tour_id)}
  tour = db.card.find_one(query)
  
  if tour:
    tour['_id'] = str(tour['_id'])
    return tour

  return jsonify({'tour': tour})

# 투어 카드 대륙별로 받아오기
@tour.route('/', methods=['GET'])
def getByContinent():
  continent = request.args.get('continent')
  tour_list = db.card.find({'continent': continent})
  for tour in tour_list:
            tour['_id'] = str(tour['_id'])
  return jsonify({'tour_list': tour_list})

# 투어 카드 수정하기
@tour.route('/<tour_id>', methods=['PUT'])
def updateTour(tour_id):
  tour_url = request.form["tour_url"]
  tour_title = request.form["tour_title"]
  tour_location = request.form["tour_location"]
  tour_continent = request.form["tour_continent"]
  tour_date = request.form["tour_date"]
  tour_content = request.form["tour_content"]

  doc = {
    "url": tour_url,
    "title": tour_title,
    "location": tour_location,
    "continent": tour_continent,
    "date": tour_date,
    "content": tour_content,
  }
  db.card.update_one({"_id": ObjectId(tour_id)}, {"$set": doc })
  return jsonify({"msg": "수정완료"})

# 카드 삭제하기
@tour.route('/<tour_id>', methods=["DELETE"])
def deleteTour(tour_id):
  db.card.delete_one({"_id": ObjectId(tour_id)})
  return jsonify({"msg": "삭제완료"})