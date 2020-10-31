from flask_wtf import FlaskForm
from password_validator import PasswordValidator
from wtforms import StringField, PasswordField, SubmitField, Field
from wtforms.validators import DataRequired, Length, ValidationError

class PasswordValid:
    def __init__(self, message: str = None):
        if not message:
            message = u'Password requirements:\n' \
                      u'Contains at least 8 characters\n' \
                      u'Contains at least a lower case letter and a digit'
        self.message = message

    def __call__(self, form: FlaskForm, field: Field):
        schema = PasswordValidator()
        schema \
            .min(8) \
            .has().lowercase() \
            .has().digits()
        if not schema.validate(field.data):
            raise ValidationError(self.message)


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired()])
    password = PasswordField(label='Password', validators=[
        DataRequired()])
    submit = SubmitField(label='Login')


class RegistrationForm(FlaskForm):
    username = StringField(label='Username', validators=[
        DataRequired(message='Username is required'),
        Length(min=3, message='Username needs to be at least 3 characters')
    ])
    password = PasswordField(label='Password', validators=[
        DataRequired(message='Password is required'),
        PasswordValid()
    ])
    submit = SubmitField(label='Register')