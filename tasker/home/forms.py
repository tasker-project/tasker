# 2020-09-23 09:56:33 -0700 - Maged Bebawy - started working on forms and models files - lines:,4,5,6,7
# 2020-09-10 17:51:11 -0400 - Jeremy Axmacher - Initial commit - lines:,3,8,9
from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, EqualTo, email
