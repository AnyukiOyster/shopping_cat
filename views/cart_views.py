from fastapi import Request, Form, Depends, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from db.shopservice import *
from views import templates
from views.dependencies import *

router = APIRouter()

#Страница корзины
@router.get("/cart", response_class=HTMLResponse)
async def view_cart(request: Request, user_id: int = Depends(show_current_user_id), context: dict = Depends(get_categories)):
    cart_items = get_cart_db(user_id)
    total_price = sum(item.goods_fk.price * item.quantity for item in cart_items) if cart_items else 0
    context["cart"] = cart_items
    context["total_price"] = total_price
    cart_warning = request.cookies.get("cart_warning")
    if cart_warning:
        context["cart_warning"] = cart_warning
    return templates.TemplateResponse("cart.html", request=request, context=context)

# Увеличение количества товара
@router.post("/cart/increase/{product_id}", response_class=HTMLResponse)
async def increase_quantity(product_id: int, user_id: int = Depends(show_current_user_id)):
    db = next(get_db())
    cart_entry = db.query(Cart).filter_by(client_id=user_id, goods_id=product_id).first()
    if cart_entry:
        result = update_cart_db(product_id, user_id, cart_entry.quantity + 1)
        if not result:
            response = RedirectResponse("/cart", status_code=303)
            response.set_cookie(key="cart_warning", value="Невозможно увеличить количество: товара недостаточно на складе.", max_age=5)
            return response
    return RedirectResponse("/cart", status_code=303)

# Уменьшение количества товара
@router.post("/cart/decrease/{product_id}", response_class=HTMLResponse)
async def decrease_quantity(product_id: int, user_id: int = Depends(show_current_user_id)):
    db = next(get_db())
    cart_entry = db.query(Cart).filter_by(client_id=user_id, goods_id=product_id).first()
    if cart_entry:
        update_cart_db(product_id, user_id, cart_entry.quantity - 1)
    return RedirectResponse("/cart", status_code=303)

# Полное удаление товара из корзины
@router.post("/cart/delete/{product_id}", response_class=HTMLResponse)
async def delete_item_from_cart(product_id: int, user_id: int = Depends(show_current_user_id)):
    delete_in_cart_db(user_id, product_id)
    return RedirectResponse("/cart", status_code=303)

# Совершение покупки
@router.post("/cart/purchase", response_class=HTMLResponse)
async def purchase(request: Request, user_id: int = Depends(show_current_user_id), context: dict = Depends(get_categories)):
    result = make_purchase_db(user_id)
    if not result["success"]:
        context["cart"] = result["cart"]
        context["warning"] = result["message"]
        return templates.TemplateResponse("cart.html", request=request, context=context)
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="purchase_message", value=result["message"], max_age=7)
    return response