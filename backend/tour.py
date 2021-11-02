from flask import Blueprint

tour = Blueprint('tour', __name__)

@tour.route('/')
def getTour():
  return "tour"