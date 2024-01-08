from flask_admin import Admin
from flask_admin.base import MenuLink

from main import db
from main.models import Post, User

from .views import PostAdminView, ProtectedAdminIndexView, UserAdminView

admin = Admin(
    name="admin", index_view=ProtectedAdminIndexView(), template_mode="bootstrap4"
)

admin.add_view(UserAdminView(User, db.session))
admin.add_view(PostAdminView(Post, db.session))
admin.add_link(MenuLink(name="Website", endpoint="main.index"))
admin.add_link(MenuLink(name="Logout", endpoint="users.logout"))
