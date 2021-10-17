from flask_wtf import FlaskForm
from wtforms import MultipleFileField, StringField, TextAreaField, SubmitField, BooleanField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired


class SiteForm(FlaskForm):
    #text = TextAreaField('Повестка дня собрания:', validators=[DataRequired()])
    images = MultipleFileField('Отчет Правления(jpg, jpeg, png, bmp, pdf):',
                               validators=[FileAllowed(['jpg', 'jpeg', 'png', "bmp", "pdf"], 'Images only!')])
    docs_image = MultipleFileField('Документы СНТ(jpg, jpeg, png, bmp, pdf):',
                                   validators=[FileAllowed(['jpg', 'jpeg', 'png', "bmp", "pdf"], 'Images only!')])
    oplata_image = MultipleFileField('Оплата членских взносов(jpg, jpeg, png, bmp, pdf):',
                             validators=[FileAllowed(['jpg', 'jpeg', 'png', "bmp", "pdf"], 'Images only!')])
    oplata_text = TextAreaField("Оплата членских взносов:", validators=[DataRequired()], default="...!")
    dolgi_text = TextAreaField("Долги по оплате членских взносов:", validators=[DataRequired()], default="...")
    submit = SubmitField('Сохранить')
# multiple
