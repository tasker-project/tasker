from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, email


class ChangeViewForm(FlaskForm):
    select_view = RadioField('select_view', default='Day', choices=[('Day', 'Day'), ('Week', 'Week'), ('Month','Month')], validators=[DataRequired()])


class SignUp(FlaskForm):
    email = StringField('Email', [DataRequired(), email()])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password', [DataRequired()])
    timezone = SelectField('Time zone', choices=[(date, 'Atlantic Standard Time (AST)'), ('EST', 'Eastern Standard Time (EST)'), ('CST', 'Central Standard Time (CST)'), ('MST', 'Mountain Standard Time (MST)'), ('PST', ' Pacific Standard Time (PST)'), ('AKST', 'Alaskan Standard Time (AKST)'), ('HST', 'Hawaii-Aleutian Standard Time (HST)'), ('UTC-11', 'Samoa standard time (UTC-11)'), ('UTC+10', 'Chamorro Standard Time (UTC+10)')])
    submit = SubmitField('submit')


class SignIn(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])