import datetime
from typing import Annotated, Optional

from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship

from database import Base, str_256

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime.datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"),
    onupdate=datetime.datetime.utcnow,
)]


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    username: Mapped[str]
    password_hash: Mapped[Optional[str]]
    email: Mapped[Optional[str]]
    created_at: Mapped[created_at]
    posts: Mapped[list["PostsORM"]] = relationship(
        back_populates="author",
    )


class PostsORM(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str_256]
    # TO DO: change type of description
    description: Mapped[str]
    # comments: Mapped[list["CommentsORM"]] = relationship()
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]

    author: Mapped["UsersORM"] = relationship(
        back_populates="posts",
    )

# class CommentsORM(Base):
#     __tablename__ = "comments"
#
#     id: Mapped[intpk]
#     author_id: Mapped[str]
#     text: Mapped[str]
#     created_at: Mapped[created_at]
#     updated_at: Mapped[updated_at]
#
#     author: Mapped["UsersORM"] = relationship()