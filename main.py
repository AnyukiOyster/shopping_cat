from fastapi import FastAPI
from db import Base, engine
from api.cart import cart_router
from api.categories import category_router
from api.clients import user_router
from api.products import goods_router
from views import router as views_router
from db.shopservice import *

# Создание базы данных
Base.metadata.create_all(engine)

# Создание основного приложения и подключение ссылок
app = FastAPI(docs_url='/docs')
app.include_router(views_router)
app.include_router(cart_router)
app.include_router(category_router)
app.include_router(user_router)
app.include_router(goods_router)