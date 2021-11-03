from flask import Blueprint, jsonify, request
from pymongo import MongoClient
from bson import ObjectId

like = Blueprint('like', __name__ )
client = MongoClient('localhost', 27017)
db = client.airtravel


@like.route('/<tour_id>', methods=['POST'])
def likeTour(tour_id):
  query= {"_id": ObjectId(tour_id)}
  tour = db.card.find_one(query)
  if tour :
    db.card.update_one({"_id": ObjectId(tour_id)}, {"$set": {"like": True} })
  
  return jsonify({"msg": "좋아요 완료"})

@like.route('/<tour_id>', methods=['DELETE'])
def dislikeTour(tour_id):
  query= {"_id": ObjectId(tour_id)}
  tour = db.card.find_one(query)
  if tour :
    db.card.update_one({"_id": ObjectId(tour_id)}, {"$set": {"like": False} })
  
  return jsonify({"msg": "좋아요 취소 완료"})
