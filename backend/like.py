from flask import Blueprint

like = Blueprint('like', __name__ )

@like.route('/')
def getTour():
  return "like"