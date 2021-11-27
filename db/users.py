import sqlalchemy

from .base import metadata

users = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer,
                      primary_key=True, autoincrement=True, unique=True),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("email", sqlalchemy.String, unique=True),
    sqlalchemy.Column("password", sqlalchemy.String),
    sqlalchemy.Column("register_date", sqlalchemy.DateTime)
)
