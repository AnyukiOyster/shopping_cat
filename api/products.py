from fastapi import APIRouter, UploadFile, File
from db.shopservice import *
from api import result_message
from pydantic import BaseModel
from typing import Optional
import random

goods_router_api = APIRouter(prefix="/api-goods", tags=["Товары"])

class ProductCreate(BaseModel):
    category_id: int
    product_name: str
    price: float
    amount: int
    in_stock: Optional[bool] = True

# Добавление нового товара
@goods_router_api.post('/add_product')
async def add_product(product_data: ProductCreate):
    product_dict = dict(product_data)
    return result_message(add_product_db(**product_dict))

# Добавление фотографии товара
@goods_router_api.post("/add_photo")
async def add_photo(product_id: int, photo_file: UploadFile = File(...)):
    file_id = random.randint(1, 1_000_000)
    if photo_file:
        with open(f"db/images/photo_{file_id}_{product_id}.jpg", "wb") as photo:
            photo_to_save = await photo_file.read()
            photo.write(photo_to_save)
            add_product_photo_db(product_id, photo.name)
            return {"status": 1, "message": "Фото успешно сохранено"}
    return {"status": 0, "message": False}

# Вывод товара
@goods_router_api.get('/show_product')
async def show_product(product_id: int):
    r = get_product_db(product_id)
    return result_message(r)

#Удаление товара
@goods_router_api.delete('/delete_product')
async def delete_product(product_id: int):
    r = delete_product_db(product_id)
    return result_message(r)

#Изменение данных товара
@goods_router_api.put('/edit_product')
async def update_product(product_id: int, field: str, info: str):
    r = update_product_db(product_id, field, info)
    return result_message(r)