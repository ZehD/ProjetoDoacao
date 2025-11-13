from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


class LoginForm(FlaskForm):
    """Formulário de login"""
    username = StringField('Usuário', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Entrar')


class RegisterForm(FlaskForm):
    """Formulário de registro"""
    username = StringField('Usuário', validators=[
        DataRequired(),
        Length(min=3, max=80, message='Usuário deve ter entre 3 e 80 caracteres')
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email(message='Email inválido')
    ])
    password = PasswordField('Senha', validators=[
        DataRequired(),
        Length(min=6, message='Senha deve ter no mínimo 6 caracteres')
    ])
    password_confirm = PasswordField('Confirmar Senha', validators=[
        DataRequired(),
        EqualTo('password', message='Senhas não coincidem')
    ])
    submit = SubmitField('Cadastrar')


class DonationItemForm(FlaskForm):
    """Formulário para um item de doação"""
    item_name = StringField('Nome do Item', validators=[DataRequired()])
    quantity = FloatField('Quantidade', validators=[
        DataRequired(),
        NumberRange(min=0.1, message='Quantidade deve ser maior que zero')
    ])
    unit = SelectField('Unidade', choices=[
        ('litro', 'Litro'),
        ('kg', 'Quilograma'),
        ('unidade', 'Unidade'),
        ('pacote', 'Pacote'),
        ('caixa', 'Caixa'),
        ('garrafa', 'Garrafa')
    ], validators=[DataRequired()])
