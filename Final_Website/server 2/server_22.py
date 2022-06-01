# docs:
# https://marshmallow-sqlalchemy.readthedocs.io/en/latest/

# imports
# sourcery skip: avoid-builtin-shadow
import hashlib
import sqlalchemy as sqla
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref
from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field
from marshmallow import pre_load
import os
from datetime import datetime
import logging
import flask

# local
import logger as logger_module


# constants:
PORT = 5000
with open('hashed_key.key', 'r') as file:
    SECRET_KEY_HASH = file.read()

# setup logger
logger_module.setup_logger(os.path.basename(__file__))
logger = logging.getLogger(os.path.basename(__file__))


# setup sql engine:
# engine = sqla.create_engine("sqlite:///:memory:")
basedir = os.path.abspath(os.path.dirname(__file__))
engine = sqla.create_engine(
    'sqlite:///' + os.path.join(basedir, 'database.db'),
    echo=True,
    future=True
)

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


# setup sqlalchemy row obj
class Reading_Uncalibrated(Base):
    """Table for uncalibrated readings"""
    __tablename__ = 'readings_uncalibrated'
    primary_key = sqla.Column(sqla.Integer, primary_key=True)
    # timestamp = sqla.Column(sqla.DateTime())
    pressure = sqla.Column(sqla.Float())
    temperature = sqla.Column(sqla.Float())
    humidity = sqla.Column(sqla.Float())
    wind_speed = sqla.Column(sqla.Float())
    wind_direction = sqla.Column(sqla.Float())
    precipitation = sqla.Column(sqla.Float())

    def __init__(self, timestamp, pressure, temperature, humidity, wind_speed, wind_direction, precipitation):
        # self.timestamp = timestamp
        self.pressure = pressure
        self.temperature = temperature
        self.humidity = humidity
        self.wind_speed = wind_speed
        self.wind_direction = wind_direction
        self.precipitation = precipitation


    def __repr__(self):
        return f"<Reading_Uncalibrated(id={self.id}, timestamp={self.timestamp})>"


# create all tables
Base.metadata.create_all(engine)

# setup marshmallow schema
class Reading_Uncalibrated_Schema(SQLAlchemySchema):
    class Meta:
        model=Reading_Uncalibrated
        load_instance=True  # Optional: deserialize to model instances
        # datetimeformat = '%Y-%m-%d %H:%M:%S'

    primary_key =auto_field()
    # timestamp=auto_field()
    pressure=auto_field()
    temperature=auto_field()
    humidity=auto_field()
    wind_speed=auto_field()
    wind_direction=auto_field()
    precipitation=auto_field()
    
    # @pre_load
    # def add_timestamp(self, data, **kwargs):
    #     print("IN PRE_LOAD")
    #     # print(type(data))
    #     # print(data)
    #     # data['timestamp'] = datetime.now()
    #     # print(data)
    #     return data

# schema objs used in serialization
reading_uncalibrated_schema = Reading_Uncalibrated_Schema()
reading_uncalibrated_schema_many = Reading_Uncalibrated_Schema(many=True)



# # functions
# def hash(plain_txt):
#     """one way hash using sha256"""
#     hash_ = hashlib.sha256()
#     hash_.update(plain_txt.encode())
#     return hash_.hexdigest()



# # setup get and post handlers
# def handle_get_readings():
#     query = sqla.select(Reading_Uncalibrated)
#     all_readings = list(session.scalars(query))
#     serialised_readings: dict = reading_uncalibrated_schema_many.dump(all_readings)
#     return flask.jsonify(serialised_readings)


# # setup app
# app = flask.Flask(__name__)
# app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



# # setup get routes
# @app.route('/get_readings', methods=['GET'])
# def get_readings():
#     return handle_get_readings()


# @app.route("/", methods=['GET'])
# def index():
#     return flask.redirect(flask.url_for("get_readings"))


# def run_app():
#     app.run(host='127.0.0.1', port=PORT, debug=True)

# if __name__ == '__main__':
#     run_app()