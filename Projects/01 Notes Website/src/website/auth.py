from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select
from werkzeug.security import check_password_hash, generate_password_hash

from .database import db_session
from .models import User

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        remember = request.form.get("remember")
        user = db_session.scalars(select(User).filter_by(email=email)).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category="success")
                login_user(user, remember=bool(remember))
                return redirect(url_for("views.index"))
            flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exists.", category="error")

    return render_template("auth/login.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.index"))


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        first_name = data.get("first_name")
        password = data.get("password")
        confirm_password = data.get("confirm_password")
        hashed_password = generate_password_hash(password)
        user = db_session.scalars(select(User).filter_by(email=email)).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif first_name and len(first_name) < 2:
            flash("First name must be greater than 1 characters.", category="error")
        elif password != confirm_password:
            flash("Passwords don't match.", category="error")
        elif len(password) < 4:
            flash("Password must be at least 4 characters.", category="error")
        else:
            flash("Account created. Now you can login.", category="sucess")
            user = User(email=email, password=hashed_password, first_name=first_name)
            db_session.add(user)
            db_session.commit()
            return redirect(url_for("auth.login"))

    return render_template("auth/signup.html")
