from fastapi import FastAPI
from db import Base, engine
from pydantic import BaseModel
from api.cart import cart_router_api
from api.categories import category_router_api
from api.clients import user_router_api
from api.products import goods_router_api
from db.shopservice import *
from fastapi.staticfiles import StaticFiles
from views.home_views import router as home_router
from views.cart_views import router as cart_router
from views.product_views import router as product_router
from views.category_views import router as category_router
from views.user_auth import router as user_auth_router

# Создание базы данных
Base.metadata.create_all(engine)

# Создание основного приложения и подключение ссылок
app = FastAPI(docs_url='/docs')
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(home_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(category_router)
app.include_router(user_auth_router)
app.include_router(user_router_api)
app.include_router(goods_router_api)
app.include_router(cart_router_api)
app.include_router(category_router_api)

"""
 Schemas 
"""

class Token(BaseModel):
    access_token: str
    token_type: str