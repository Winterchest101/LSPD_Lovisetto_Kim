# Importing necessary modules and libraries
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, Session
from flask_login import UserMixin, login_user, LoginManager, login_required
from flask_login import current_user, logout_user
from forms import CreateCarForm, CreateNewUser, LoginUser
from forms import CommentForm, ReservationForm
from flask_gravatar import Gravatar
from sqlalchemy import create_engine
from functools import wraps
from sqlalchemy.ext.declarative import declarative_base
import os

# Initializing Flask app
app = Flask(__name__)

# Setting secret key for Flask app
app.config['SECRET_KEY'] = 'ewrfnirawu4hiqufrnwa2ne'

# Initializing CKEditor and Bootstrap extensions
ckeditor = CKEditor(app)
Bootstrap(app)

# Initializing Gravatar extension for user avatars
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)


# Wrapper function for admin access control
def admin(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated and current_user.role == 'uploader':
            return function(*args, **kwargs)
        else:
            return abort(403)
    return wrapper


# Setting up database URI and disabling track modifications
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL?sslmode=require", "sqlite:///car.db"
    )
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializing SQLAlchemy database
db = SQLAlchemy(app)

# Initializing Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Creating SQLAlchemy engine and session
engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///car.db"))
session = Session(engine)


# Loading user by ID for Flask-Login
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# Base class for declarative models
Base = declarative_base()


# User model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), unique=True, nullable=False)
    role = db.Column(db.String(50), default='renter', nullable=False)
    cars = relationship("Car", back_populates="owner")
    comments = relationship("Comment", back_populates="owner_comments")
    reservations = relationship("Reservation", back_populates="user")


# Reservation model
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


# Car model
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


# Method to create dictionary representation of Car object
def create_dict(self):
    return {
        column.name: getattr(self, column.name)
        for column in self.__table__.columns
    }


# Comment model
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    car_id = db.Column(db.Integer, db.ForeignKey('cars.id'))
    owner_comments = relationship("User", back_populates="comments")
    car_comments = relationship("Car", back_populates="comments")
    text = db.Column(db.Text, nullable=False)


# Creating all tables in the database
db.create_all()


# User registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = CreateNewUser()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash(
                "You already signed up with that email! Try to login instead!",
                category='error'
                  )
            return redirect(url_for('login'))
        else:
            user = User(
                name=form.name.data,
                password=generate_password_hash(
                    password=form.password.data,
                    method='pbkdf2:sha256',
                    salt_length=8),
                email=form.email.data,
                role=form.role.data
            )
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash("Successfully registered!", category='error')
            return redirect(url_for('get_all_cars'))
    return render_template(
        "register.html", form=form, logged_in=current_user.is_authenticated)


# User login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginUser()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for('get_all_cars'))
            else:
                flash(
                    message="Password is invalid, try again!",
                    category="error")
                return redirect(url_for('login'))
        else:
            flash(message="There is no user with that email, try again!",
                  category="error")
            return redirect(url_for('login'))
    return render_template("login.html",
                           form=form,
                           logged_in=current_user.is_authenticated)


# User logout route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_cars'))


# Route to get all cars
@app.route('/')
def get_all_cars():
    cars = Car.query.filter_by(is_rented=False)
    is_admin = False
    if current_user.is_authenticated and current_user.role == 'uploader':
        is_admin = True
    return render_template("index.html",
                           all_cars=cars,
                           logged_in=current_user.is_authenticated,
                           admin=is_admin)


# Route to show a specific car post
@app.route("/post/<int:car_id>", methods=['GET', 'POST'])
def show_post(car_id):
    form = CommentForm()
    is_admin = False
    if current_user.is_authenticated and current_user.role == 'uploader':
        is_admin = True
    car = Car.query.get(car_id)
    if form.validate_on_submit():
        if not current_user.is_authenticated:
            flash(
                message="To leave a comment, you need to login first!",
                category="error")
            return redirect(url_for('login'))
        else:
            comment = Comment(
                text=form.user_comment.data,
                owner_comments=current_user,
                car_comments=car,
            )
            db.session.add(comment)
            db.session.commit()
            form.user_comment.data = ''
    return render_template("post.html",
                           car=car,
                           logged_in=current_user.is_authenticated,
                           admin=is_admin,
                           form=form)


# Route to display user's rentals
@app.route("/your_rents")
def your_renting():
    return render_template("your_rents.html",
                           logged_in=current_user.is_authenticated)


# Route to display rented cars
@app.route("/rented")
def rented():
    auth = current_user.is_authenticated
    role = current_user.role
    cars = Car.query.filter_by(is_rented=True)
    is_admin = False
    if auth and role == 'uploader':
        is_admin = True
    return render_template("rented.html",
                           all_cars=cars,
                           logged_in=current_user.is_authenticated,
                           admin=is_admin)


# Route to add a new car post
@app.route("/new-post", methods=['GET', 'POST'])
def add_new_post():
    form = CreateCarForm()
    if form.validate_on_submit():
        new_post = Car(
            mark=form.Mark.data,
            model=form.Model.data,
            body=form.body.data,
            img_url=form.img_url.data,
            owner=current_user,
            transmission=form.Transmission.data,
            category=form.Category.data,
            date=date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_cars"))
    return render_template("make-post.html",
                           form=form,
                           logged_in=current_user.is_authenticated)


# Route to edit a car post
@app.route("/edit-post/<int:car_id>", methods=['GET', 'POST'])
@admin
def edit_post(car_id):
    car = Car.query.get(car_id)
    edit_form = CreateCarForm(
        Mark=car.mark,
        Model=car.model,
        body=car.body,
        category=car.category,
        transmission=car.transmission,
        img_url=car.img_url,
    )
    if edit_form.validate_on_submit():
        car.mark = edit_form.Mark.data
        car.model = edit_form.Model.data
        car.body = edit_form.body.data
        car.img_url = edit_form.img_url.data
        car.category = edit_form.Category.data
        car.transmission = edit_form.Transmission.data
        db.session.commit()
        return redirect(url_for("show_post", car_id=car.id))

    return render_template("make-post.html",
                           orm=edit_form,
                           logged_in=current_user.is_authenticated,
                           car=car)


# Route to delete a car post
@app.route("/delete/<int:car_id>")
@admin
def delete_post(car_id):
    post_to_delete = Car.query.get(car_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_cars'))


# Route to rent a car
@app.route("/rent/<int:car_id>")
def rent_car(car_id):
    car = Car.query.get(car_id)
    car.is_rented = True
    db.session.commit()
    return redirect(url_for("show_post", car_id=car.id))


# Route to reserve a car
@app.route("/reserve/<int:car_id>", methods=['GET', 'POST'])
@login_required
def reserve_car(car_id):
    car = Car.query.get(car_id)
    if car.is_rented:
        flash("Car is already rented.", category='error')
        return redirect(url_for("get_all_cars"))

    form = ReservationForm()
    if form.validate_on_submit():
        reservation = Reservation(
            user=current_user,
            car=car,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        car.is_rented = True
        db.session.add(reservation)
        db.session.commit()
        flash("Car reserved successfully!", category='success')
        return redirect(url_for("get_all_cars"))

    return render_template("reserve-car.html",
                           form=form,
                           car=car,
                           logged_in=current_user.is_authenticated)


# Running the app
if __name__ == "__main__":
    app.run(debug=True, port=3000)
