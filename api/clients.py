from fastapi import APIRouter
from db.userservice import *
from pydantic import BaseModel
from api import result_message

user_router = APIRouter(prefix="/api-users", tags=["База клиентов магазина"])

class UserCreate(BaseModel):
    name: str
    tel: str
    password: str
    surname: str = None

@user_router.post("/add_user")
async def add_user(user_data: UserCreate):
    user_dict = dict(user_data)
    return result_message(add_user_db(**user_dict))

@user_router.get("/get_user")
async def get_exact_user(user_id):
    result = get_exact_user_db(user_id)
    return result_message(result)

@user_router.delete("/delete_user")
async def delete_user(user_id: int):
    result = delete_user_db(user_id)
    return result_message(result)


@user_router.put("/update_user")
async def update_user(user_id: int, change_info: str, new_info: str):
    result = update_user_db(user_id, change_info, new_info)
    return result_message(result)