# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,4,5,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
# 2020-09-19 18:16:30 -0700 - Emily Martens - add JS functionality, add change view front end controls and styles - lines:,3,6,7,8
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, email

class ChangeViewForm(FlaskForm):
    select_view = RadioField('select_view', default='Day', choices=[('Day', 'Day'), ('Week', 'Week'), ('Month','Month')], validators=[DataRequired()])


class SignUp(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), email()])
    time_zone = SelectField('Time zone', choices=[('AST', 'Atlantic Standard Time (AST)'), ('EST', 'Eastern Standard Time (EST)'), ('CST', 'Central Standard Time (CST)'), ('MST', 'Mountain Standard Time (MST)'), ('PST', ' Pacific Standard Time (PST)'), ('AKST', 'Alaskan Standard Time (AKST)'), ('HST', 'Hawaii-Aleutian Standard Time (HST)'), ('UTC-11', 'Samoa standard time (UTC-11)'), ('UTC+10', 'Chamorro Standard Time (UTC+10)')])
    submit = SubmitField('submit')


class SignIn(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
