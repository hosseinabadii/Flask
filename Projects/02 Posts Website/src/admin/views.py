from flask import redirect, request, url_for
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class ProtectedAdminIndexView(AdminIndexView):
    def is_visible(self):
        return False

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("users.login", next=request.url))
        return redirect(url_for("main.index"))


class BaseAdminView(ModelView):
    can_view_details = True
    create_modal = True
    edit_modal = True
    details_modal = True

    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("users.login", next=request.url))
        return redirect(url_for("main.index"))


class UserAdminView(BaseAdminView):
    column_list = ["username", "email", "role"]
    column_searchable_list = ["username", "email"]
    form_excluded_columns = ["password"]


class PostAdminView(BaseAdminView):
    column_list = [
        "title",
        "date_posted",
        "content",
        "is_public",
        "image_file",
        "author",
        "author_id",
    ]
    column_sortable_list = [
        "title",
        "date_posted",
        "content",
        "is_public",
        "image_file",
        "author_id",
    ]
    column_searchable_list = ["title", "author_id"]
    form_columns = ["title", "content", "is_public", "author"]
    form_ajax_refs = {
        "author": {
            "fields": ["id", "username", "email"],
            "page_size": 10,
        }
    }
