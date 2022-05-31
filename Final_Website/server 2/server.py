from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


#initliazing our flask app, SQLAlchemy and Marshmallow
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////datastore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
ma = Marshmallow(app)


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


data_reading_schema = Data_Reading_Schema()
data_reading_schema_many = Data_Reading_Schema(many=True)


# #adding a post
# @app.route('/post', methods=['POST'])
# def add_post():
#     title = request.json['title']
#     description = request.json['description']
#     author = request.json['author']

#     my_posts = Post(title, description, author)
#     db.session.add(my_posts)
#     db.session.commit()

#     return post_schema.jsonify(my_posts)


#getting posts
@app.route('/get', methods=['GET'])
def get_post():
    all_posts = Data_Reading.query.all()
    result = data_reading_schema_many.dump(all_posts)

    return jsonify(result)


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
    app.run(debug=True)
