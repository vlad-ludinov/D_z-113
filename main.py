from sqlalchemy import select

from db import Users, Products, Orders, app, new_session
from models import User, UserIn, Product, ProductIn, Order, OrderIn
from fastapi import FastAPI, Path
import uvicorn


# @app.on_event("startup")
# async def startup():
#     await database.connect()
#
#
# @app.on_event("shutdown")
# async def shutdown():
#     await database.disconnect()


@app.get("/users/", response_model=list[User])
async def get_users():
    async with new_session() as session:
        query = select(Users)
        result = await session.execute(query)
        users_model = result.scalars().all()
        return users_model


# @app.get("/users/", response_model=list[User])
# async def get_users():
#     query = users.select()
#     return await database.fetch_all(query)


@app.get("/users/{user_id}/", response_model=User)
async def get_user_by_id(user_id: int = Path(...)):
    async with new_session() as session:
        # result = await session.get(Users, user_id)
        # return result
        query = select(Users).filter(Users.id == user_id)
        result = await session.execute(query)
        user_model = result.scalars().one()
        return user_model


# @app.get("/users/{user_id}/", response_model=User)
# async def get_user_by_id(user_id: int = Path(...)):
#     query = users.select().where(users.c.id == user_id)
#     return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    async with new_session() as session:
        new_user = Users(**user.dict())
        session.add(new_user)
        await session.flush()
        await session.commit()
    return {"id": new_user.id, **user.dict()}


# @app.post("/users/", response_model=User)
# async def create_user(user: UserIn):
#     query = users.insert().values(**user.dict())
#     last_record_id = await database.execute(query)
#     return {"id": last_record_id, **user.dict()}


@app.put("/users/{user_id}/", response_model=User)
async def edit_user(new_user: UserIn, user_id: int = Path(...)):
    async with new_session() as session:
        query = select(Users).filter(Users.id == user_id)
        result = await session.execute(query)
        user_model = result.scalars().one()
        user_model.name = new_user.name
        user_model.surname = new_user.surname
        user_model.email = new_user.email
        user_model.password = new_user.password
        await session.commit()
        return user_model


# @app.put("/users/{user_id}/", response_model=User)
# async def edit_user(new_user: UserIn, user_id: int = Path(...)):
#     query = users.update().where(users.c.id == user_id).values(**new_user.dict())
#     await database.execute(query)
#     return {"id": user_id, **new_user.dict()}


@app.delete("/users/{user_id}/")
async def delete_user(user_id: int = Path(...)):
    async with new_session() as session:
        query = select(Users).filter(Users.id == user_id)
        result = await session.execute(query)
        user_model = result.scalars().one()
        await session.delete(user_model)
        await session.commit()
        return {'message': 'User deleted'}


# @app.delete("/users/{user_id}/")
# async def delete_user(user_id: int = Path(...)):
#     query = users.delete().where(users.c.id == user_id)
#     await database.execute(query)
#     return {'message': 'User deleted'}


#
#
#


@app.get("/products/", response_model=list[Product])
async def get_products():
    async with new_session() as session:
        query = select(Products)
        result = await session.execute(query)
        products_model = result.scalars().all()
        return products_model


@app.get("/products/{product_id}/", response_model=Product)
async def get_product_by_id(product_id: int = Path(...)):
    async with new_session() as session:
        query = select(Products).filter(Products.id == product_id)
        result = await session.execute(query)
        product_model = result.scalars().one()
        return product_model


@app.post("/products/", response_model=Product)
async def create_product(product: ProductIn):
    async with new_session() as session:
        new_product = Products(**product.dict())
        session.add(new_product)
        await session.flush()
        await session.commit()
    return {"id": new_product.id, **product.dict()}


@app.put("/products/{product_id}/", response_model=Product)
async def edit_product(new_product: ProductIn, product_id: int = Path(...)):
    async with new_session() as session:
        query = select(Products).filter(Products.id == product_id)
        result = await session.execute(query)
        product_model = result.scalars().one()
        product_model.name = new_product.name
        product_model.description = new_product.description
        product_model.price = new_product.price
        await session.commit()
        return product_model


@app.delete("/products/{product_id}/")
async def delete_product(product_id: int = Path(...)):
    async with new_session() as session:
        query = select(Products).filter(Products.id == product_id)
        result = await session.execute(query)
        product_model = result.scalars().one()
        await session.delete(product_model)
        await session.commit()
        return {'message': 'Product deleted'}


#
#
#


@app.get("/orders/", response_model=list[Order])
async def get_orders():
    async with new_session() as session:
        query = select(Orders)
        result = await session.execute(query)
        orders_model = result.scalars().all()
        return orders_model


@app.get("/orders/{order_id}/", response_model=Order)
async def get_order_by_id(order_id: int = Path(...)):
    async with new_session() as session:
        query = select(Orders).filter(Orders.id == order_id)
        result = await session.execute(query)
        order_model = result.scalars().one()
        return order_model


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    async with new_session() as session:
        new_order = Orders(**order.dict())
        session.add(new_order)
        await session.flush()
        await session.commit()
    return {"id": new_order.id, **order.dict()}


@app.put("/orders/{order_id}/", response_model=Order)
async def edit_order(new_order: OrderIn, order_id: int = Path(...)):
    async with new_session() as session:
        query = select(Orders).filter(Orders.id == order_id)
        result = await session.execute(query)
        order_model = result.scalars().one()
        order_model.user_id = new_order.user_id
        order_model.product_id = new_order.product_id
        order_model.status = new_order.status
        order_model.date = new_order.date
        await session.commit()
        return order_model


@app.delete("/orders/{order_id}/")
async def delete_order(order_id: int = Path(...)):
    async with new_session() as session:
        query = select(Orders).filter(Orders.id == order_id)
        result = await session.execute(query)
        order_model = result.scalars().one()
        await session.delete(order_model)
        await session.commit()
        return {'message': 'Order deleted'}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

