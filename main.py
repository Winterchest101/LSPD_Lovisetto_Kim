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

class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    # role = db.Column(db.String(50), default='renter', nullable=False)
    cars = relationship("Car", back_populates="owner")
    comments = relationship("Comment", back_populates="owner_comments")
    reservations = relationship("Reservation", back_populates="user")

class Reservation(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    user = relationship("User", back_populates="reservations")
    car = relationship("Car", back_populates="reservations")

class Car(db.Model):
    __tablename__ = "cars"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    owner = relationship("User", back_populates="cars")
    comments = relationship("Comment", back_populates="car_comments")
    reservations = relationship("Reservation", back_populates="car")
    mark = db.Column(db.String(250), unique=True, nullable=False)
    model = db.Column(db.String(250), nullable=False)
    category = db.Column(db.String(250), nullable=False)
    transmission = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    is_rented = db.Column(db.Boolean, default=False, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    
#user
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateNewUser()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash("You already signed up with that email! Try to login instead!", category='error')
            return redirect(url_for('login'))
        else:
            user = User(
                name=form.name.data,
                password=generate_password_hash(password=form.password.data, method='pbkdf2:sha256', salt_length=8),
                email=form.email.data,
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('get_all_cars'))
    return render_template("register.html", form=form, logged_in=current_user.is_authenticated)