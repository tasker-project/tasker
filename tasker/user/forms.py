from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField, RadioField
from wtforms.validators import DataRequired, EqualTo, Email


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
