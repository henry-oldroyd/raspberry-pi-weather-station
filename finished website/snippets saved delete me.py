

with open('server/hashed_key.key', 'r') as file:
    SECRET_KEY_HASH = file.read()

# setup app
app = flask.Flask(
    __name__,
    # static_url_path='',
    # static_folder='static',
    # template_folder='templates'
    static_folder='../static',
    template_folder='../templates'
)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


# setup sql engine:
# basedir = os.path.abspath(os.path.dirname(__file__))
# https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
engine = sqla.create_engine(
    # 'sqlite:///' + os.path.join(basedir, './database.db'),
    'sqlite:///database.db',
    # "sqlite:///:memory:",
    echo=True,
    future=True,
    connect_args={'check_same_thread': False}
)

return flask.redirect(flask.url_for("static", filename=f"images/{name}.png"))
