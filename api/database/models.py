# from sqlalchemy import MetaData
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey



class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    lang: Mapped[str]


class Creator(Base):
    __tablename__ = "creators"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    skill: Mapped[str]
    is_busy: Mapped[bool] = True


class OrderType(Base):
    __tablename__ = "ordertypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class CreatorOrderType(Base):
    __tablename__ = "creator_ordertype"
    id: Mapped[int] = mapped_column(primary_key=True)
    ordertype_id: Mapped[int] = mapped_column(ForeignKey("ordertypes.id"))
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.tg_id"))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.tg_id"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    work_type: Mapped[str]


class Admin(Base):
    __tablename__ = "admins"
    tg_id: Mapped[str] = mapped_column(primary_key=True)
