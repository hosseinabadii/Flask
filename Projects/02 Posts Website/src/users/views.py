from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from main import services
from main.models import User

from .forms import LoginFrom, RegistrationFrom, UpdateAccountFrom
from .utils import save_picture

users = Blueprint(
    "users",
    __name__,
    static_folder="static",
    static_url_path="/users/static",
    template_folder="templates",
)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = RegistrationFrom()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=username, email=email, password=hashed_password)
        services.add(user)
        flash("Your account has been created! Now you can login.", "success")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))

    form = LoginFrom()
    if form.validate_on_submit():
        user = services.get_first_filter_by(User, email=form.email.data)
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Logged in successfully!", category="success")
            return redirect(next_page or url_for("main.index"))
        flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", form=form)


@users.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountFrom()
    if form.validate_on_submit():
        if form.picture.data:
            current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        services.update()
        flash("Your account has been updated!", "success")
        return redirect(url_for("users.account"))
    form.username.data = current_user.username
    form.email.data = current_user.email
    image_file = url_for(
        "users.static", filename=f"profile_pics/{current_user.image_file}"
    )
    return render_template("account.html", image_file=image_file, form=form)
