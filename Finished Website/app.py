from server import server

FLASK_APP = server.app
print("http://127.0.0.1:5000/")
FLASK_APP.run(host='127.0.0.1', port=5000)
