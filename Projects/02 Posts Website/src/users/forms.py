from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from sqlalchemy import select
from wtforms import (
    BooleanField,
    PasswordField,
    StringField,
    SubmitField,
    ValidationError,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length

from main import db
from main.models import User


class RegistrationFrom(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", [DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = db.session.scalars(
            select(User).filter_by(username=username.data)
        ).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        user = db.session.scalars(select(User).filter_by(email=email.data)).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginFrom(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])
    password = PasswordField("Password", [DataRequired()])
    remember = BooleanField("Remember me", default=False)
    submit = SubmitField("Login")


class UpdateAccountFrom(FlaskForm):
    username = StringField("Username", [DataRequired(), Length(min=2, max=20)])
    email = StringField("Email", [DataRequired(), Email()])
    picture = FileField(
        "Update Profile Picture",
        [FileAllowed(["png", "jpg", "jpeg"])],
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data == current_user.username:
            return
        user = db.session.scalars(
            select(User).filter_by(username=username.data)
        ).first()
        if user:
            raise ValidationError(
                "That username is taken. Please choose a different one."
            )

    def validate_email(self, email):
        if email.data == current_user.email:
            return
        user = db.session.scalars(select(User).filter_by(email=email.data)).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class RequestResetForm(FlaskForm):
    email = StringField("Email", [DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        user = db.session.scalars(select(User).filter_by(email=email.data)).first()
        if user is None:
            raise ValidationError("There is no account with that email.")


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password", [DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")
