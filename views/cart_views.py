from fastapi import Request, Form, Depends
from fastapi.responses import RedirectResponse
from db.shopservice import *
from views import templates, router
from views.dependencies import get_categories

# Получение айди текущего пользователя
def get_current_user():
    # Тут будет функция для вычисления зарегистрированного пользователя
    return 1

#Страница корзины
@router.get("/cart")
async def view_cart(request: Request, user_id: int = Depends(get_current_user), context: dict = Depends(get_categories)):
    context["cart"] = get_cart_db(user_id)
    return templates.TemplateResponse("cart.html", request=request, context=context)

# Увеличение количества товара
@router.post("/cart/increase/{product_id}")
async def increase_quantity(product_id: int, user_id: int = Depends(get_current_user)):
    cart = get_cart_db(user_id)
    for item in cart:
        if item.goods_id == product_id:
            update_cart_db(product_id, user_id, item.quantity + 1)
            break
    return RedirectResponse("/cart", status_code=303)

# Уменьшение количества товара
@router.post("/cart/decrease/{product_id}")
async def decrease_quantity(product_id: int, user_id: int = Depends(get_current_user)):
    cart = get_cart_db(user_id)
    for item in cart:
        if item.goods_id == product_id:
            update_cart_db(product_id, user_id, item.quantity - 1)
            break
    return RedirectResponse("/cart", status_code=303)

# Полное удаление товара из корзины
@router.post("/cart/delete/{product_id}")
async def delete_item_from_cart(product_id: int, user_id: int = Depends(get_current_user)):
    delete_in_cart_db(user_id, product_id)
    return RedirectResponse("/cart", status_code=303)

# # Совершение покупки
# @router.post("/cart/make_purchase")
# async def make_purchase(user_id: int = Depends(get_current_user), cart = Depends(view_cart)):
#     sum = 0
#     message = []
#     for item in cart:
#         same_product = get_product_db(item.goods_id)
#         if same_product.amount - item.quantity < 0:
#             s = [same_product.product_name, same_product.amount]
#             message.append[s]
#     if len(message)>0:
#         return RedirectResponse("/cart", {'error': })
#         sum += item.quantity * same_product.price
#
#     clear_cart_db(user_id)
#     return RedirectResponse("/cart", status_code=303)