import os

from dotenv import load_dotenv

load_dotenv(".env")


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    SECURITY_PASSWORD_SALT = os.getenv("SECURITY_PASSWORD_SALT")
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USE_TLS = os.getenv("MAIL_USE_TLS")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    FLASK_ADMIN_SWATCH = os.getenv("FLASK_ADMIN_SWATCH")
    FLASK_ADMIN_FLUID_LAYOUT = os.getenv("FLASK_ADMIN_FLUID_LAYOUT")
