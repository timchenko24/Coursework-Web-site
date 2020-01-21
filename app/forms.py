from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from wtforms.validators import Required, DataRequired


class RegisterForm(Form):
    name = StringField('Name', validators=[validators.Length(min=7, max=30)])
    username = StringField('Username', validators=[validators.Length(min=7, max=20)])
    email = StringField('E-mail', validators=[validators.Email()])
    password = PasswordField('Password', validators=[validators.Length(min=7, max=20),
                                                     validators.EqualTo('confirm', message='Do not match')])
    confirm = PasswordField('Confirm password')

class ClientForm(Form):
    fio = StringField('Имя', validators=[validators.Length(min=7, max=100)])
    address = StringField('Адрес', validators=[validators.Length(min=7, max=100)])
    phone = StringField('Телефон', validators=[validators.Length(min=7, max=30)])
    email = StringField('E-mail', validators=[validators.Email()])