import flask
# import json
import os
import hashlib
import logging
import flask
from flask_cors import CORS
import sqlite3 as sql
from datetime import datetime


# local
import logger as logger_module

# setup logger
logger_module.setup_logger(os.path.basename(__file__))
logger = logging.getLogger(os.path.basename(__file__))

# would be sotred hashed
with open('hashed_key.key', 'r') as file:
    SECRET_KEY_HASH = file.read()
PORT = 80
logger.info(f"fetched secret key hash: {SECRET_KEY_HASH}")
logger.info(f"Using port {PORT}")


def hash(plain_txt):
    """one way hash using sha256"""
    hash_ = hashlib.sha256()
    hash_.update(plain_txt.encode())
    return hash_.hexdigest()

# # read data
# def read_data(data_category):
#     logger.info("reading all data from data store")
#     with open("./data.json", "r") as file:
#         result = json.loads(file.read())
#     logger.info(f"all data store contents:  {result}")
#     if data_category:
#         logger.info(f"data category was specified as {data_category} filtering out other data")
#         result = [data_item[data_category] for data_item in result]
#     else:
#         logger.info("no data category specified no filter needed")

#     result = tuple(result)
#     logger.info(f"Get request will return:  {result}")
#     return result

# # append data point
# def append_data(data_item):
#     logger.info(f"appending data item  {data_item} to data store")
#     # read existing data
#     with open("./data.json", "r") as file:
#         data = json.load(file)
#     # append new item
#     data.append(data_item)
#     # rewrite
#     with open("./data.json", "w") as file:
#         json.dump(data, file)



def if_not_exists_make_table():
    with open(".\sql_stored_rocedures\create_table.sql", "r") as file:
        cmd = file.read()
    with sql.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute(cmd)
        connection.commit()
        
def get_all_from_db():
    with sql.connect("database.db") as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT TIMESTAMP, RAIN, LIGHT FROM WEATHER")
        result = cursor.fetchall()
        connection.commit()
    # convert row form to dictionary record
    # depends on table order
    def row_to_record(row):
        return {"timestamp": row[0], "rain": row[1], "light": row[2]}
    result = tuple(row_to_record(row) for row in result)
    return result

# should prevent hte possibility of sql injections
# https: // realpython.com/prevent-python-sql-injection/
def get_category_from_db(category):
    with sql.connect("database.db") as connection:
        cursor = connection.cursor()
        # cursor.execute(
        #     "SELECT %(row)s FROM WEATHER",
        #     {"row": category}
        # )
        cursor.execute(
            "SELECT ? FROM WEATHER",
            category
        )
        result = cursor.fetchall()
        connection.commit()
    # convert row form to dictionary record
    def row_to_record(row):
        return {category: row[0]}
    result = tuple(row_to_record(row) for row in result)
    return result

def sql_add_item_to_table(data_item):
    now = datetime.now()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
    with sql.connect("database.db") as connection:
        cursor = connection.cursor()
        # cursor.execute(
        #     """
        #         INSERT INTO WEATHER (TIMESTAMP, RAIN, LIGHT)
        #         VALUES
        #             %(new_row)s
        #     """,
        #     {"new_row": (timestamp, data_item["rain"], data_item["light"])}
        # )
        cursor.execute(
            """
                INSERT INTO WEATHER (TIMESTAMP, RAIN, LIGHT)
                VALUES (?, ?, ?)
            """,
            (timestamp, data_item["rain"], data_item["light"])
        )
        connection.commit()


# read data
def read_data(data_category):
    logger.info("reading all data from data store")
    if data_category:
        logger.info(f"data category was specified as {data_category} filtering out other data")
        result = get_category_from_db(data_category)
    else:
        logger.info("no data category specified no filter needed")
        result = get_all_from_db()
    
    result = tuple(result)
    logger.info(f"Get request will return:  {result}")
    return result

# append data point
def append_data(data_item):
    logger.info(f"appending data item  {data_item} to data store")
    sql_add_item_to_table(data_item)


# create flask app
app = flask.Flask(
    __name__,
    static_folder=os.path.abspath('../website/static'),
    template_folder=os.path.abspath('../website/templates'),
)
CORS(app)
logger.info("flask app object created")


def handle_get(data_category):
    if not data_category:
        logger.info("Responding to get request with all data")
        return read_data(None)
    else:
        try:
            assert data_category in ["light", "rain"], "data_category invalid"
        except AssertionError as e:
            logger.exception(e)
            raise
        else:
            logger.info("data argument recognised")
        data = read_data(data_category)
        logger.info("responding with just this data")
        logger.info(data)
        return data


def verify_pi_key(secret_key) -> bool:
    hashed_key = hash(secret_key)
    logger.info(f"the hash received key:  {hashed_key}")

    if hashed_key == SECRET_KEY_HASH:
        logger.info("secret key correct after hash comparrison")
        return True
    else:
        logger.warning("secret key wrong for post request")
        return False


def handle_post(secret_key, new_data_item):
    logger.info(f"server received new data:  {new_data_item}")
    output_safe_secret_key = secret_key[:4] + "*"*(len(secret_key)-8) + secret_key[-4:]
    logger.info(f"server received new secret key:  {output_safe_secret_key}")

    if verify_pi_key(secret_key):
        logger.info("data item added to data store")
        logger.info("returning all data")
        append_data(new_data_item)
        return read_data(None)
    else:
        logger.warning("aborting with 401 authentication failed")
        flask.abort(401)


@app.route("/data", methods=['GET', 'POST'])
@app.route("/data/<data_category>", methods=['GET', 'POST'])
def data(data_category=None):
    if data_category:
        data_category = data_category.lower()
        assert data_category in ("all", "rain", "light")
        if data_category == "all":
            data_category = None
    
    method = flask.request.method
    
    logger.info(f"Route data used with method  {method}")
    if method == "GET":
        logger.info(f"Data category argument given as {data_category}")
        if data_category:
            data_category = data_category.lower()
        method = flask.request.method
        return str(handle_get(data_category))

    if method == "POST":
        data_header = flask.request.json
        secret_key = data_header["secret_key"]
        new_data_item = data_header["new_data_item"]
        return str(handle_post(secret_key, new_data_item))



# @app.route("/")
# def main():
#     logger.info("Route main used with GET method")
#     logger.info("Rendering and returning html home page")

#     rendered = flask.render_template("index.html")
#     # vue meant to also use {{ }} but it instead now uses {({})}
#     rendered = rendered.replace("{({", "{{").replace("})}", "}}")
#     return rendered


logger.info("all flask routes defined")
if __name__ == "__main__":
    if_not_exists_make_table()
    sample_data = (
        {"rain": 0.67, "light": 0.45},
        {"rain": 0.42, "light": 0.21},
        {"rain": 0.99, "light": 0.03},
        {"rain": 0.34, "light": 0.22},
    )
    for sample_item in sample_data:
        append_data(sample_item)
    logger.info("running flask app")
    app.run(host='127.0.0.1', port=PORT)
