import pydantic
from pydantic import BaseModel, Field, EmailStr


class User(BaseModel):
    id: int
    name: str = Field(..., min_length=4, max_length=16)
    surname: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=128)


class UserIn(BaseModel):
    name: str = Field(..., min_length=4, max_length=16)
    surname: str = Field(min_length=4, max_length=16)
    email: EmailStr
    password: str = Field(..., min_length=4, max_length=128)


class Product(BaseModel):
    id: int
    name: str = Field(..., min_length=4, max_length=16)
    description: str = Field(None, max_length=256)
    price: int = Field(..., ql=0)


class ProductIn(BaseModel):
    name: str = Field(..., min_length=4, max_length=16)
    description: str = Field(None, max_length=256)
    price: int = Field(..., ql=0)


class Order(BaseModel):
    id: int
    user_id: int
    product_id: int
    date: pydantic.PastDate
    status: bool = Field(False)


class OrderIn(BaseModel):
    user_id: int
    product_id: int
    date: pydantic.PastDate
    status: bool = Field(False)
