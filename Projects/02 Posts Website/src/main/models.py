import enum
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, DateTime, Enum, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from main import db


class Roles(enum.Enum):
    ADMINISTRATOR = "administrator"
    # EDITOR = "editor"
    AUTHOR = "author"


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    image_file: Mapped[str] = mapped_column(
        String(20), nullable=False, default="default.png"
    )
    password: Mapped[str] = mapped_column(String(60))
    role: Mapped[Roles] = mapped_column(Enum(Roles), default=Roles.AUTHOR)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

    @property
    def is_admin(self):
        return self.role == Roles.ADMINISTRATOR

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, username={self.username!r}, email={self.email!r})"

    def __str__(self) -> str:
        return self.username


class Post(db.Model):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    date_posted: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    image_file: Mapped[str] = mapped_column(
        String(120), nullable=False, default="default_thumbnail.jpg"
    )
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")

    def __repr__(self) -> str:
        return f"Post(id={self.id!r}, title={self.title!r}, date_posted={self.date_posted!r})"

    def __str__(self) -> str:
        return self.title
