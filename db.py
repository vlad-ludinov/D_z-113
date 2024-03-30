import datetime

import databases
import sqlalchemy
from fastapi import FastAPI
from sqlalchemy import func, Column, Integer, String, Boolean, ForeignKey, Date
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column








# import uvicorn

# pip install sqlalchemy
# pip install databases[aiosqlite]

DATABASE_URL = "sqlite+aiosqlite:///new_database.db"
# database = databases.Database(DATABASE_URL)
# metadata = sqlalchemy.MetaData()

engine = sqlalchemy.ext.asyncio.create_async_engine(DATABASE_URL)
new_session = async_sessionmaker(engine, expire_on_commit=False)

# Base = declarative_base()


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]


# class Users(Base):
#     __tablename__ = "users"
#     id = Column(Integer, primary_key=True),
#     name = Column(String(16)),
#     surname = Column(String(16)),
#     email = Column(String(32)),
#     password = Column(String(128))


# users = sqlalchemy.Table(
#     "Users",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("name", sqlalchemy.String(16)),
#     sqlalchemy.Column("surname", sqlalchemy.String(16)),
#     sqlalchemy.Column("email", sqlalchemy.String(32)),
#     sqlalchemy.Column("password", sqlalchemy.String(128))
# )


class Products(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]


# class Products(Base):
#     __tablename__ = "products"
#     id = Column(Integer, primary_key=True),
#     name = Column(String(16)),
#     description = Column(String(256)),
#     price = Column(Integer)


# products = sqlalchemy.Table(
#     "Products",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("name", sqlalchemy.String(16)),
#     sqlalchemy.Column("description", sqlalchemy.String(256)),
#     sqlalchemy.Column("price", sqlalchemy.Integer)
# )


class Orders(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    date: Mapped[datetime.date] = mapped_column(Date, server_default=func.current_date())
    status: Mapped[bool] = mapped_column(default=False)


# class Orders(Base):
#     __tablename__ = "orders"
#     id = Column(Integer, primary_key=True),
#     user_id = Column(ForeignKey("users.id")),
#     product_id = Column(ForeignKey("products.id")),
#     date = Column(Date, default=func.current_date),
#     status = Column(Boolean, default=False)


# orders = sqlalchemy.Table(
#     "Orders",
#     metadata,
#     sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
#     sqlalchemy.Column("user_id", sqlalchemy.ForeignKey("users.id")),
#     sqlalchemy.Column("product_id", sqlalchemy.ForeignKey("products.id")),
#     sqlalchemy.Column("date", sqlalchemy.Date, default=func.current_date),
#     sqlalchemy.Column("status", sqlalchemy.Boolean, default=False)
# )


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def delete_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")


app = FastAPI(lifespan=lifespan)


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()
#
#
# if __name__ == "__main__":
#     uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
