from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from views import templates
from views.dependencies import get_categories
from db.shopservice import *
import random

from views.user_auth import get_current_user

router = APIRouter()

# Функция для вывода 4 случайных товаров на главной
def random_goods():
    goods = get_product_db(0)
    amount_goods = len(goods)
    if amount_goods == 0:
        return []
    elif amount_goods <= 4:
        return [product.id for product in goods]
    else:
        return random.sample([product.id for product in goods], 4)

    #Главная страница
@router.get('/', response_class=HTMLResponse)
async def main(request: Request, context: dict = Depends(get_categories), current_user: Client = Depends(get_current_user)):
    print(context)
    random_ids = random_goods()
    context["products_showing"] = [get_product_db(prod_id) for prod_id in random_ids if get_product_db(prod_id)]
    purchase_message = request.cookies.get("purchase_message")
    if purchase_message:
        context["purchase_message"] = purchase_message
    return templates.TemplateResponse(name='home.html', request=request, context=context)