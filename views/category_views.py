from fastapi import Request, Depends, APIRouter
from fastapi.responses import HTMLResponse
from views import templates
from views.dependencies import get_categories
from db.shopservice import *

router = APIRouter()

#Страница отдельной категории товаров
@router.get('/categories/{category_id}', response_class=HTMLResponse)
async def single_category(request: Request, category_id: int, context: dict = Depends(get_categories)):
    category_data = get_exact_category_db(category_id)
    if category_data:
        context["category"] = category_data["category"]
        context["products"] = category_data["products"]
        return templates.TemplateResponse(name='single_category.html', request=request, context=context)
    context["message"] = "Категория не найдена"
    return templates.TemplateResponse("single_category.html", request=request, context=context)