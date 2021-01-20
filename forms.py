from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Optional, EqualTo


class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[
                             DataRequired(), EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')
    email = StringField("Email", validators=[DataRequired()])
    birthday = DateField('Birthday', format='%Y-%m-%d',
                         validators=(Optional(),))
    submit = SubmitField('Sign Up')


class SigninForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Sign In')


class AdminMovieAddForm(FlaskForm):
    movie_title = StringField("Title", validators=[DataRequired()])
    movie_description = StringField("Description", validators=[Optional()])
    movie_image = StringField("Image Link", validators=[Optional()])
    submit = SubmitField('Add Movie')


class AdminMovieUpdateForm(FlaskForm):
    movie_title = StringField("Title", validators=[DataRequired()])
    movie_description = StringField("Description", validators=[DataRequired()])
    movie_image = StringField("Image Link", validators=[DataRequired()])
    submit = SubmitField('Update Movie')


class AddFriendForm(FlaskForm):
    friend_username = StringField(
        "Friend Username", validators=[DataRequired()])
    submit = SubmitField('Add Friend')
