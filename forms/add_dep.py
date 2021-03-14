from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class DepForm(FlaskForm):
    chief = IntegerField('Глава', validators=[DataRequired()])
    title = StringField('Название', validators=[DataRequired()])
    members = StringField('Сотрудники')
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Принять')
