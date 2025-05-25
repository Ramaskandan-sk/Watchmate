from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, URL, Length, Optional, ValidationError
import re

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message='Password must be at least 6 characters long')
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match')
    ])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

def validate_image_path(form, field):
    # First check if it's a URL
    url_pattern = r'^(https?:\/\/)?((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|((\d{1,3}\.){3}\d{1,3}))(\:\d+)?(\/[-a-z\d%_.~+]*)*(\?[;&a-z\d%_.~+=-]*)?(\#[-a-z\d_]*)?$'
    local_path_pattern = r'^(img|static/img|/img|/static/img)/[\w\-/.]+\.(jpg|jpeg|png|gif|svg|webp)$'
    
    if not (re.match(url_pattern, field.data, re.I) or re.match(local_path_pattern, field.data, re.I)):
        raise ValidationError('Please enter a valid URL or local image path (e.g., img/image.jpg)')

class AddWatchlistItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    image_url = StringField('Image URL/Path', validators=[DataRequired(), validate_image_path])
    category = SelectField('Category', choices=[
        ('Movie', 'Movie'), 
        ('Anime', 'Anime'), 
        ('Series', 'Series')
    ], validators=[DataRequired()])
    submit = SubmitField('Add to Watchlist')

class EditWatchlistItemForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    image_url = StringField('Image URL/Path', validators=[DataRequired(), validate_image_path])
    category = SelectField('Category', choices=[
        ('Movie', 'Movie'), 
        ('Anime', 'Anime'), 
        ('Series', 'Series')
    ], validators=[DataRequired()])
    submit = SubmitField('Update Watchlist Item')