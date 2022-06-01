# from flask import Flask, redirect, request, jsonify, url_for
import hashlib
import flask
import flask_marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from datetime import datetime

# initialing our flask app, SQLAlchemy and Marshmallow
app = flask.Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/datastore.db'
basedir = os.path.abspath(os.path.dirname(__file__))
# print(os.path.join(basedir, 'database.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Added to prevent browser caching and update CSS, etc. in browser when editing
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

db = SQLAlchemy(app)
ma = Marshmallow(app)


with open('hashed_key.key', 'r') as file:
    SECRET_KEY_HASH = file.read()
PORT = 5000
# logger.info(f"fetched secret key hash: {SECRET_KEY_HASH}")
# logger.info(f"Using port {PORT}")


#this is our database model
class Data_Reading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime())
    pressure = db.Column(db.Float())
    temperature = db.Column(db.Float())
    humidity = db.Column(db.Float())
    wind_speed = db.Column(db.Float())
    wind_direction = db.Column(db.Float())
    precipitation = db.Column(db.Float())

    def __init__(self, timestamp, pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
        self.timestamp = timestamp
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation


class Data_Reading_Schema(ma.Schema):
    class Meta:
        fields = ('timestamp', 'pressure', 'temperature', 'humidity', 'wind_speed', 'wind_direction', 'precipitation')
        # https://stackoverflow.com/questions/53606872/datetime-format-in-flask-marshmallow-schema
        datetimeformat = '%Y-%m-%d %H:%M:%S'

    @flask_marshmallow.pre_load
    def add_timestamp(self, data, **kwargs):    
        data['timestamp'] = datetime.now()
        return data

data_reading_schema = Data_Reading_Schema()
data_reading_schema_many = Data_Reading_Schema(many=True)




def hash(plain_txt):
    """one way hash using sha256"""
    hash_ = hashlib.sha256()
    hash_.update(plain_txt.encode())
    return hash_.hexdigest()


#adding a post
@app.route('/add_reading', methods=['POST'])
def add_post():
    data_header = flask.request.json
    print("server received data")
    print(data_header)

    secret_key = data_header["secret_key"]
    new_reading_data: dict = data_header["new_data_item"]
    
    if hash(secret_key) != SECRET_KEY_HASH:
        print("secret key wrong for post request")
        flask.abort(401)
    
    new_reading_obj = data_reading_schema.load(new_reading_data)

    db.session.add(new_reading_obj)
    db.session.commit()

    return data_reading_schema.jsonify(new_reading_obj)


#getting posts
@app.route('/get_data', methods=['GET'])
def get_data():
    all_posts = Data_Reading.query.all()
    result = data_reading_schema_many.dump(all_posts)

    return flask.jsonify(result)

@app.route("/", methods=['GET'])
def index():
    return flask.redirect(flask.url_for("get_data"))

# #getting particular post
# @app.route('/post_details/<id>/', methods=['GET'])
# def post_details(id):
#     post = Post.query.get(id)
#     return post_schema.jsonify(post)


# #updating post
# @app.route('/post_update/<id>/', methods=['PUT'])
# def post_update(id):
#     post = Post.query.get(id)

#     title = request.json['title']
#     description = request.json['description']
#     author = request.json['author']

#     post.title = title
#     post.description = description
#     post.author = author

#     db.session.commit()
#     return post_schema.jsonify(post)


# #deleting post
# @app.route('/post_delete/<id>/', methods=['DELETE'])
# def post_delete(id):
#     post = Post.query.get(id)
#     db.session.delete(post)
#     db.session.commit()

#     return post_schema.jsonify(post)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=PORT, debug=True)
