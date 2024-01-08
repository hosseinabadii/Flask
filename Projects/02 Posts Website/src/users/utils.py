from pathlib import Path

from flask import current_app, url_for
from flask_login import current_user
from flask_mail import Message
from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer
from PIL import Image

from main import ROOT_PATH, mail


def save_picture(form_picture):
    suffix = Path(form_picture.filename).suffix
    picture_filename = f"user{current_user.id}_profile" + suffix
    picture_path = ROOT_PATH / f"static/users/profile_pics/{picture_filename}"
    image = Image.open(form_picture)
    image.thumbnail(size=(125, 125))
    image.save(picture_path)

    return picture_filename


def generate_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def send_password_reset_email(user_email, reset_token):
    msg = Message(
        "Password Reset Request",
        sender="noreply@yourdomain.com",
        recipients=[user_email],
    )
    reset_url = url_for("users.reset_token", token=reset_token, _external=True)
    msg.body = f"To reset your password, visit the following link: \n{reset_url}"
    mail.send(msg)
    # print(msg)


def verify_reset_token(token, expiration=1800):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except (SignatureExpired, BadSignature):
        return None
