# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,8,14,15,49,50
# 2020-09-19 18:16:30 -0700 - Emily Martens - add JS functionality, add change view front end controls and styles - lines:,7,10,12,13
# 2020-09-27 13:28:53 -0700 - Emily Martens - fix naming discrepancies in user forms/views/templates, add form styling classes to register template, restructure login and register templates to match, re-enable User blueprint. - lines:,9,16,17,20,21,22,24,26,28,29,31,33,35,36,38,40,42,43,45,48,51,52,53,54
# 2020-09-26 08:00:34 -0700 - Maged Bebawy - fixed timezones - lines:,23,25,27,30,32,37,39,41,44,46,47
# 2020-09-26 08:06:19 -0700 - Maged Bebawy - fixed timezones - lines:,34
# 2020-09-25 07:30:26 -0700 - Maged Bebawy - added user registeration - lines:,11,18,19
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email


class ChangeViewForm(FlaskForm):
    select_view = RadioField('select_view', default='Day', choices=[('Day', 'Day'), ('Week', 'Week'), ('Month','Month')], validators=[DataRequired()])


class SignUpForm(FlaskForm):
    email_address = StringField('Email', [DataRequired(), Email()])
    password = PasswordField('Password', [DataRequired(), EqualTo('confirm_password', message='Passwords must match')])
    confirm_password = PasswordField('Confirm password', [DataRequired()])
    timezone = SelectField('Timezone', choices=[('America/Adak', 'America/Adak'), ('America/Anchorage', 'America/Anchorage'),
    ('America/Boise', 'America/Boise'),
    ('America/Chicago', 'America/Chicago'),
    ('America/Denver', ' America/Denver'),
    ('America/Detroit', 'America/Detroit'),
    ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'),
    ('America/Indiana/Knox', 'America/Indiana/Knox'),
    ('America/Indiana/Marengo', 'America/Indiana/Marengo'),
    ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'),
    ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'),
    ('America/Indiana/Vevay', 'America/Indiana/Vevay'),
    ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'),
    ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'),
    ('America/Indiana/Winamac', 'America/Indiana/Winamac'),
    ('America/Juneau', 'America/Juneau'),
    ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'),
    ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'),
    ('America/Los_Angeles', ' America/Los_Angeles'),
    ('America/Menominee', 'America/Menominee'),
    ('America/Metlakatla', 'America/Metlakatla'),
    ('America/New_York', 'America/New_York'),
    ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'),
    ('America/North_Dakota/Center', 'America/North_Dakota/Center'),
    ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'),
    ('America/Phoenix', 'America/Phoenix'),
    ('America/Sitka', 'America/Sitka'),
    ('America/Yakutat', 'America/Yakutat'),
    ])
    submit = SubmitField('Register')


class SignInForm(FlaskForm):
    email_address = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
