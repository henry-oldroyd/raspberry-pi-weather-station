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

# https://stackoverflow.com/questions/27234593/setting-up-static-folder-path-in-flask
app = flask.Flask(__name__, static_url_path="/static", static_folder="static")


@app.route("/data")
def data():
    return json.dumps(sample_data)


@app.route("/")
def main():
    return flask.render_template("index.html")


if __name__ == "__main__":
    print("George, go here in browser to see your website:")
    print("http://127.0.0.1:5000/")
    app.run(host='127.0.0.1', port=5000)
