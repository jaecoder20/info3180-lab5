from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import InputRequired
from flask_wtf.file import FileField,FileRequired,FileAllowed


class MovieForm(FlaskForm):
    title = StringField('Movie Title', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    poster = FileField('Upload Poster', validators=[
        FileRequired(message='Please upload movie poster'),
        FileAllowed(['jpg', 'png'], message='Only JPEG and PNG images are allowed.')
    ])