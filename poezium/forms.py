from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class PoemForm(FlaskForm):
    title = StringField('Назва', validators=[DataRequired()])
    body = TextAreaField('Текст', validators=[DataRequired()])
    author = StringField('Автор (необов’язково)')
    submit = SubmitField('Опублікувати')
