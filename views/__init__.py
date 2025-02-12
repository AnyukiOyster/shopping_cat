from fastapi.templating import Jinja2Templates
from fastapi import APIRouter

# Создание пути для HTML-шаблонов для всего пакета views
templates = Jinja2Templates(directory="templates")
router = APIRouter()