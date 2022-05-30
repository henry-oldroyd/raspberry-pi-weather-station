from flask import Flask, request, render_template, send_file, abort
import json
import os

# read data
def read_json():
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


with open("../images/images.json", "r") as file:
    image_paths = json.loads(file.read())
print(image_paths)

app = Flask(
    __name__,
    static_folder='../static',
    template_folder='../templates'
)

# Added to prevent browser caching and update CSS, etc. in browser when editing 
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.errorhandler(404)
def page_not_found(error):
    return "404: page not found", 404

@app.route("/data", methods=['GET', 'POST'])
def data():
    if request.method == "GET":
        print("server sending reponce to get request:")
        print(read_json())
        return read_json()
    if request.method == "POST":
        data_header  = request.json
        print("server received data")
        print(data_header)
        secret_key = data_header["secret_key"]
        new_data_item = data_header["new_data_item"]
        if secret_key != "123abc":
            print("secret key wrong for post request")
            return "Wrong key!"
        append_data(new_data_item)
        return str(read_json())

@app.route("/images/<name>", methods=["GET"])
def give_photo(name):
    print(name)
    try:
        assert name in image_paths.keys()
        file_path = image_paths[name]
        assert os.path.exists(file_path)
    except AssertionError:
        abort(404)
    else:
        return send_file(file_path, mimetype='image/gif')


@app.route("/")
def main():
    # return f"<p>Main website</p><br/> <a href={flask.url_for('data')}>see the data</a>"
    return render_template("index.html")



if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
