from flask_wtf import FlaskForm
from wtforms import PasswordField, BooleanField, SubmitField, StringField
from wtforms.fields.html5 import EmailField, IntegerField, DateTimeField
from wtforms.validators import DataRequired


class JobForm(FlaskForm):
    team_leader = IntegerField('Капитан', validators=[DataRequired()])
    job = StringField('Описание', validators=[DataRequired()])
    work_size = IntegerField('Длительность', validators=[DataRequired()])
    collaborators = StringField('Помошники')
    is_finished = BooleanField('Статус')
    submit = SubmitField('Принять')
