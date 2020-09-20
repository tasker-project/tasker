from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired

class ChangeViewForm(FlaskForm):
    select_view = RadioField('select_view', default='Day', choices=[('Day', 'Day'), ('Week', 'Week'), ('Month','Month')], validators=[DataRequired()])
