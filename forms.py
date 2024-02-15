# Importing necessary modules and libraries
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms import SelectField, DateField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField


# WTForm
class CreateCarForm(FlaskForm):
    # Define form fields for creating a car
    Mark = StringField("Mark of the car", validators=[DataRequired()])
    Model = StringField("Model of the car", validators=[DataRequired()])
    # Define choices for the category dropdown
    Category_choices = [
        ("economy", "Economy"),
        ("standard", "Standard"),
        ("premium", "Premium")]
    Category = SelectField(
        "Category",
        choices=Category_choices,
        validators=[DataRequired()]
        )
    # Define choices for the transmission dropdown
    Transmission_choices = [("automatic", "Automatic"), ("manual", "Manual")]
    Transmission = SelectField("Transmission",
                               choices=Transmission_choices,
                               validators=[DataRequired()])
    img_url = StringField(
        "Car's Image URL",
        validators=[DataRequired(),
                    URL()])
    # CKEditor field for car content
    body = CKEditorField("Car Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")


# Form for creating a new user
class CreateNewUser(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    # Dropdown for selecting user role
    role_choices = [("uploader", "Uploader"), ("renter", "Renter")]
    role = SelectField(
        "Role",
        choices=role_choices,
        validators=[DataRequired()])
    submit = SubmitField("Sign up")


# Form for logging in a user
class LoginUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


# Form for adding a comment
class CommentForm(FlaskForm):
    user_comment = CKEditorField(
        "Comment", validators=[DataRequired()]
        )
    submit = SubmitField("Submit comment")


# Form for making a reservation
class ReservationForm(FlaskForm):
    start_date = DateField(
        'Start Date',
        validators=[DataRequired()],
        render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField(
        'End Date',
        validators=[DataRequired()],
        render_kw={"placeholder": "YYYY-MM-DD"})
    submit = SubmitField("Reserve")
