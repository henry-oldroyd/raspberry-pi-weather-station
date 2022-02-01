# this is here to return some random weather data to Georges website so he can test his code that makes get requests
import flask
import json
from random import randint

def create_data_unit():
    return {
        "temperature": randint(0,25),
        "humidity": randint(0, 100) 
    }


sample_data = [create_data_unit() for _ in range(10)]

app = flask.Flask(__name__)


@app.route("/data")
def data():
    return json.dumps(sample_data)


# @app.route("/")
# def main():
#     return flask.render_template("test backend.html")


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
