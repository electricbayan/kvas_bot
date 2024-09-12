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
    url: Mapped[str] = mapped_column(unique=True, nullable=False)


class Creator(Base):
    __tablename__ = "creators"
    tg_id: Mapped[str] = mapped_column(unique=True, primary_key=True)
    is_busy: Mapped[bool]
    username: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)


class SkillType(Base):
    __tablename__ = "skilltypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[int]


class CreatorSkillType(Base):
    __tablename__ = "creators_skilltypes"
    id: Mapped[int] = mapped_column(primary_key=True)
    skilltype_id: Mapped[int] = mapped_column(ForeignKey("skilltypes.id", ondelete='CASCADE'))
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.tg_id", ondelete='CASCADE'))


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("creators.tg_id"), nullable=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.tg_id"))
    order_type: Mapped[str]
    description: Mapped[str]
    is_payed: Mapped[bool] = mapped_column(default=False)
    token: Mapped[str]


class Admin(Base):
    __tablename__ = "admins"
    tg_id: Mapped[str] = mapped_column(primary_key=True)


class UniqueToken(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_value: Mapped[str]
