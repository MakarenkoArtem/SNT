from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, TextAreaField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired


class EventForm(FlaskForm):
    text = TextAreaField('Событие:', validators=[DataRequired()])
    znach = BooleanField('Важное событие')
    images = MultipleFileField('Отчет Правления:',
                               validators=[FileAllowed(['jpg', 'png', "bmp"], 'Images only!')])
    submit = SubmitField('Сохранить')
# multiple
