from fastapi import APIRouter
from db.shopservice import *
from api import result_message

category_router_api = APIRouter(prefix="/api-categories", tags=["Категории товаров"])

# Добавление новой категории
@category_router_api.post('/add_category')
async def add_category(category_name: str):
    r = add_category_db(category_name)
    return result_message(r)

# Вывод всех товаров в категории
@category_router_api.get('/show_category')
async def show_category(category_id: int):
    r = get_exact_category_db(category_id)
    return result_message(r)

# Удаление категории
@category_router_api.delete('/show_category')
async def delete_category(category_id: int):
    r = delete_category_db(category_id)
    return result_message(r)