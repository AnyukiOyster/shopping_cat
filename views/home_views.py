from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from views import templates, router
from views.dependencies import get_categories
from db.shopservice import *
import random


# Функция для вывода 4 случайных товаров на главной
def random_goods():
    goods = get_product_db(0)
    amount_goods = int(len(goods))
    if amount_goods > 4:
        random_nums = random.sample(range(1, amount_goods), 4)
        return random_nums
    else:
        return 1, 2, 3, 4

#Главная страница
@router.get('/', response_class=HTMLResponse)
async def main(request: Request, context: dict = Depends(get_categories)):
    num1, num2, num3, num4 = random_goods()
    context["products_showing"] = [get_product_db(num1), get_product_db(num2), get_product_db(num3), get_product_db(num4)]
    context["all_categories"] = get_all_categories_db()
    return templates.TemplateResponse(name='home.html', request=request, context=context)