from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято.')

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Это почта уже используется.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить')
    submit = SubmitField('Войти')

class MenuItemForm(FlaskForm):
    name = StringField('Название', validators=[DataRequired()])
    description = TextAreaField('Описание')
    price = FloatField('Цена', validators=[DataRequired()])
    submit = SubmitField('Добавить')

class OrderForm(FlaskForm):
    address = StringField('Адрес', validators=[DataRequired()])
    phone_number = StringField('Номер телефона', validators=[DataRequired()])
    special_instructions = TextAreaField('Предпочтения')
    submit = SubmitField('Разместить заказ')