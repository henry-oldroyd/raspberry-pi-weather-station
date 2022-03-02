import flask
import json
import os
import hashlib
import logging

# local
import logger as logger_module

# setup logger
logger_module.setup_logger('pi_emulator')
logger = logging.getLogger('pi_emulator')

# would be sotred hashed
with open('hashed_key.key', 'r') as file:
    SECRET_KEY_HASH = file.read()
PORT = 5000


def hash(plain_txt):
    """one way hash using sha256"""
    hash_ = hashlib.sha256()
    hash_.update(plain_txt.encode())
    return hash_.hexdigest()

# read data
def read_data():
    with open("./data.json", "r") as file:
        # return json.load(file)
        return file.read()

# append data point
def append_data(data_item):
    # read existing data
    with open("./data.json", "r") as file:
        data = json.load(file)
    # append new item
    data.append(data_item)
    # rewrite
    with open("./data.json", "w") as file:
        json.dump(data, file)



app = flask.Flask(
    __name__,
    static_folder= os.path.abspath('../website/static'),
    template_folder= os.path.abspath('../website/templates'),
)

@app.route("/data", methods=['GET', 'POST'])
def data():
    if flask.request.method == "GET":
        print("server sending reponce to get request:")
        print(read_data())
        return read_data()

    if flask.request.method == "POST":
    
        data_header  = flask.request.json
        print("server received data")
        print(data_header)
        secret_key = data_header["secret_key"]
        new_data_item = data_header["new_data_item"]

        if hash(secret_key) != SECRET_KEY_HASH:
            print("secret key wrong for post request")
            flask.abort(401)

        append_data(new_data_item)
        return str(read_data())


@app.route("/")
def main():
    # return f"<p>Main website</p><br/> <a href={flask.url_for('data')}>see the data</a>"
    return flask.render_template("test backend.html")



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=PORT)
