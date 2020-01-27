from wtforms import Form, StringField, TextAreaField, PasswordField, validators, IntegerField, DateField, SelectField
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


class ProductForm(Form):
    name = StringField('Наименование', validators=[validators.Length(min=7, max=100)])
    price = IntegerField('Цена', validators=[validators.NumberRange(1, 10000)])
    number = IntegerField('Кол-во', validators=[validators.NumberRange(1, 1000)])


class SaleForm(Form):
    sale_date = DateField('Дата продажи', format='%Y-%m-%d')
    delivery_date = DateField('Дата доставки', format='%Y-%m-%d')
    number = IntegerField('Кол-во', validators=[validators.NumberRange(1, 1000)])


class QueryForm(Form):
    query = TextAreaField('SQL-запрос')