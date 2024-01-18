from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField, DateField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

## Forms
class CreateCarForm(FlaskForm):
    Mark = StringField("Mark of the car", validators=[DataRequired()])
    Model = StringField("Model of the car", validators=[DataRequired()])
    Category_choices = [("economy", "Economy"), ("standard", "Standard"), ("premium", "Premium")]
    Category = SelectField("Category", choices=Category_choices, validators=[DataRequired()])
    Transmission_choices = [("automatic", "Automatic"), ("manual", "Manual")]
    Transmission = SelectField("Transmission", choices=Transmission_choices, validators=[DataRequired()])
    img_url = StringField("Car's Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField("Car Content", validators=[DataRequired()])
    submit = SubmitField("Submit Post")

class CreateNewUser(FlaskForm):
    name = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    role_choices = [("uploader", "Uploader"), ("renter", "Renter")]
    role = SelectField("Role", choices=role_choices, validators=[DataRequired()])
    submit = SubmitField("Sign up")


class LoginUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Sign in")


class CommentForm(FlaskForm):
    user_comment = CKEditorField("Comment", validators=[DataRequired()])
    submit = SubmitField("Submit comment")


class ReservationForm(FlaskForm):
    start_date = DateField('Start Date', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    end_date = DateField('End Date', validators=[DataRequired()], render_kw={"placeholder": "YYYY-MM-DD"})
    submit = SubmitField("Reserve")