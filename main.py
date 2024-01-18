from flask import Flask, render_template, redirect, url_for, flash, jsonify, request, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ewrfnirawu4hiqufrnwa2ne'
ckeditor = CKEditor(app)
Bootstrap(app)
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

def admin(function):
    @wraps(function)
    def fun(*args, **kwargs):
        if current_user.id == 1:
            return function(*args, **kwargs)
        else:
            return abort(403)
    return fun

    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL?sslmode=require", "sqlite:///blog.db")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///blog.db"))
session = Session(engine)

@login_manager.user_loader
def get_user(id):
    return User.query.get(int(id))

Base = declarative_base()