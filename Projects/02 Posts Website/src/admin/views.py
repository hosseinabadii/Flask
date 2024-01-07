from flask import redirect, request, url_for
from flask_admin import Admin, AdminIndexView
from flask_admin.base import MenuLink
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user

from main import db
from main.models import Post, User


class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.is_admin

    def inaccessible_callback(self, name, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for("users.login", next=request.url))
        return redirect(url_for("main.index"))


admin = Admin(name="admin", index_view=MyAdminIndexView(), template_mode="bootstrap4")


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
    column_searchable_list = ["username", "email"]


class PostAdminView(BaseAdminView):
    column_list = (
        "title",
        "date_posted",
        "content",
        "is_public",
        "image_file",
        "author_id",
        "author",
    )
    column_sortable_list = (
        "title",
        "date_posted",
        "content",
        "is_public",
        "image_file",
        "author_id",
    )
    column_searchable_list = ["title", "author_id"]
    form_columns = ["title", "content", "is_public", "author"]
    form_ajax_refs = {
        "author": {
            "fields": ["id", "username", "email"],
            "page_size": 10,
        }
    }


admin.add_view(UserAdminView(User, db.session))
admin.add_view(PostAdminView(Post, db.session))
admin.add_link(MenuLink(name="Website", endpoint="main.index"))
admin.add_link(MenuLink(name="Logout", endpoint="users.logout"))
