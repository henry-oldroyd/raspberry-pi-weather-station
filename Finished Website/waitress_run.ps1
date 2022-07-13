# https://flask.palletsprojects.com/en/2.1.x/deploying/waitress/
python -m venv venv
. venv/bin/activate
pip install .
pip install waitress
waitress-serve app:app --host 127.0.0.1
waitress-serve --call app:create_app --host 127.0.0.1