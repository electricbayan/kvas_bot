# from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    lang: Mapped[str]


class Artist(Base):
    __tablename__ = "artists"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    # portfolio: Mapped[]

class Admin(Base):
    __tablename__ = "admins"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)