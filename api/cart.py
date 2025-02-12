from fastapi import APIRouter
from db.shopservice import *
from api import result_message

cart_router = APIRouter(prefix="/api-cart", tags=["Корзина"])

#Добавление товара в корзину
@cart_router.post('/to-cart')
async def add_to_cart(user_id: int, product_id: int, quantity: int):
    r = add_to_cart_db(user_id, product_id, quantity)
    return result_message(r)

#Вывод корзины клиента
@cart_router.post('/show-cart')
async def show_cart(user_id: int):
    r = get_cart_db(user_id)
    return result_message(r)

#Удаление товара из корзины
@cart_router.delete('/delete-cart')
async def delete_cart(user_id: int, prod_id: int):
    r = delete_in_cart_db(user_id, prod_id)
    return result_message(r)

#Изменение количества товара в корзине
@cart_router.put('/edit-cart')
async def edit_cart(user_id: int, prod_id: int, info: int):
    r = update_cart_db(user_id, prod_id, info)
    return result_message(r)

#Очистка корзины
@cart_router.delete('/clear-cart')
async def clear_cart(user_id: int):
    r = clear_cart_db(user_id)
    return result_message(r)