from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed

class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    poster = FileField('Poster', validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Images only!')])
