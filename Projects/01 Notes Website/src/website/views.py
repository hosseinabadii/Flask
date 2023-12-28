import json

from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import select

from .database import db_session
from .models import Note

views = Blueprint("views", __name__, static_folder="static")


@views.route("/")
def index():
    public_notes = db_session.scalars(select(Note).filter_by(is_public=True)).all()
    return render_template("index.html", public_notes=public_notes)


@views.route("/all-notes")
@login_required
def all_notes():
    return render_template("note/all_notes.html")


@views.route("/create-note", methods=["GET", "POST"])
@login_required
def create_note():
    if request.method == "POST":
        text = request.form.get("text")
        is_public = request.form.get("is_public")
        if len(text) < 1:
            flash("Note is too short!", category="error")
        else:
            user_id = current_user.id
            note = Note(text=text, user_id=user_id, is_public=bool(is_public))
            db_session.add(note)
            db_session.commit()
            flash("Note added!", category="success")
            return render_template("note/all_notes.html")

    return render_template("note/create_note.html")


@views.route("/edit-note/<int:note_id>", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = db_session.get(Note, note_id)

    if note and note.user_id == current_user.id:
        if request.method == "POST":
            updated_text = request.form.get("text")
            is_public = request.form.get("is_public")

            if len(updated_text) < 1:
                flash("Note is too short!", category="error")
            else:
                note.text = updated_text
                note.is_public = bool(is_public)
                db_session.commit()
                flash("Note updated!", category="success")
                return redirect(url_for("views.all_notes"))
        return render_template("note/edit_note.html", note=note)
    flash("Note not found or you don't have permission to edit it.", category="error")
    return redirect(url_for("views.all_notes"))


@views.route("/delete-note", methods=["POST"])
@login_required
def delete_note():
    note_id = json.loads(request.data)["note_id"]
    db_note = db_session.get(Note, note_id)
    if db_note and db_note.user_id == current_user.id:
        db_session.delete(db_note)
        db_session.commit()

    return jsonify({})
