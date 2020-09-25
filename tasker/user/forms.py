from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email

class ChangeViewForm(FlaskForm):
    select_view = RadioField('select_view', default='Day', choices=[('Day', 'Day'), ('Week', 'Week'), ('Month','Month')], validators=[DataRequired()])


class SignUp(FlaskForm):
    user_name = StringField('Username', validators=[DataRequired()])
    first_name = StringField('First name', validators=[DataRequired()])
    last_name = StringField('Last name', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    time_zone = SelectField('Time zone', choices=[('AST', 'Atlantic Standard Time (AST)'), ('EST', 'Eastern Standard Time (EST)'), ('CST', 'Central Standard Time (CST)'), ('MST', 'Mountain Standard Time (MST)'), ('PST', ' Pacific Standard Time (PST)'), ('AKST', 'Alaskan Standard Time (AKST)'), ('HST', 'Hawaii-Aleutian Standard Time (HST)'), ('UTC-11', 'Samoa standard time (UTC-11)'), ('UTC+10', 'Chamorro Standard Time (UTC+10)')])
    submit = SubmitField('submit')


class SignInForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
