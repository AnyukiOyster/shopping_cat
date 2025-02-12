from fastapi import Request, Depends
from fastapi.responses import HTMLResponse
from views import templates, router
from views.dependencies import get_categories
from db.shopservice import *

#Страница отдельного товара
@router.get('/products/{product_id}', response_class=HTMLResponse)
async def single_product(request: Request, product_id: int, context: dict = Depends(get_categories)):
    context["product"] = get_product_db(product_id)
    return templates.TemplateResponse(name='single_product.html', request=request, context=context)

# for product in products:
#     print(product.product_name)
#     for photo in product.photos:
#         print(photo.photo_file)