from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, declarative_base, mapped_column, relationship

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(150), nullable=False)
    first_name: Mapped[str] = mapped_column(String(150), nullable=False)
    notes: Mapped[list["Note"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User-{self.id} {self.email}"


class Note(Base):
    __tablename__ = "note"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    text: Mapped[str] = mapped_column(String(10000))
    date: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    is_public: Mapped[bool] = mapped_column(Boolean, default=False)
    user: Mapped["User"] = relationship(back_populates="notes")

    def __str__(self):
        return f"Note-{self.id} for {self.date}"
