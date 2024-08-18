# from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from typing import List



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    tg_id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    lang: Mapped[str]


class Creator(Base):
    __tablename__ = "creators"
    tg_id: Mapped[int] = mapped_column(unique=True, primary_key=True)
    load: Mapped[int]
    work_types: Mapped[List[str]]


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.tg_id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    work_type: Mapped[str]
