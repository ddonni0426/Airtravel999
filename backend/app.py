from flask import Flask, render_template

from like import like
from auth import auth
from tour import tour

app = Flask(__name__, template_folder='../frontend/src')
app.register_blueprint(tour, url_prefix="/tour")
app.register_blueprint(like, url_prefix="/like")
app.register_blueprint(auth, url_prefix="/auth")


@app.route('/')
def home():
	return render_template('index.html')

if __name__ == '__main__':
	app.run('0.0.0.0',port=5050,debug=True)
