from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from views import templates
from views.dependencies import *
from db.shopservice import *

router = APIRouter()

#Страница отдельного товара
@router.get('/products/{product_id}', response_class=HTMLResponse)
async def single_product(request: Request, product_id: int, context: dict = Depends(get_categories)):
    context["product"] = get_product_db(product_id)
    return templates.TemplateResponse(name='single_product.html', request=request, context=context)

#Добавление товара в корзину
@router.post('/products/{product_id}/to-cart')
async def add_product_to_cart(product_id: int, quantity: int = 1, user_id: int = Depends(get_current_user)):
    result = add_to_cart_db(user_id, product_id, quantity)
    if not result:
        response = RedirectResponse("/products/{product_id}", status_code=303)
        response.set_cookie(key="message_warning", value="Товар не удалось добавить в корзину.", max_age=5)
        return response
    response = RedirectResponse("/products/{product_id}", status_code=303)
    response.set_cookie(key="message_success", value="Товар добавлен в корзину.", max_age=5)
    return response