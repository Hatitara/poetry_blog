from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class PoemForm(FlaskForm):
    title = StringField('Назва', validators=[DataRequired()])
    body = TextAreaField('Текст', validators=[DataRequired()])
    tags = StringField('Теги (через кому або з #)', render_kw={"placeholder": "#кохання, #життя"})
    category = StringField('Категорія', render_kw={"placeholder": "Наприклад: любов, філософія"})
    is_draft = BooleanField('Зберегти як чернетку')
    submit = SubmitField('Опублікувати')

