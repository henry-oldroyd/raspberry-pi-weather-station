from waitress import serve
from server import server

FLASK_APP = server.app
print("http://127.0.0.1:5000/")
# serve(FLASK_APP, host='0.0.0.0', port=8080)
serve(FLASK_APP, host='127.0.0.1', port=5000)
