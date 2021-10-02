from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, TextAreaField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired


class SiteForm(FlaskForm):
    #text = TextAreaField('Повестка дня собрания:', validators=[DataRequired()])
    images = MultipleFileField('Отчет Правления:',
                               validators=[FileAllowed(['jpg', 'png', "bmp"], 'Images only!')])
    docs_image = MultipleFileField('Документы СНТ:',
                                   validators=[FileAllowed(['jpg', 'png', "bmp"], 'Images only!')])
    oplata_image = FileField('Оплата членских взносов:',
                             validators=[FileAllowed(['jpg', 'png', "bmp"], 'Images only!')])
    oplata_text = TextAreaField("Оплата членских взносов:", validators=[DataRequired()], default="...")
    dolgi_image = FileField('Долги по оплате членских взносов:',
                            validators=[FileAllowed(['jpg', 'png', "bmp"], 'Images only!')])
    submit = SubmitField('Сохранить')
# multiple
