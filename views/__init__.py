from fastapi.templating import Jinja2Templates

# Создание пути для HTML-шаблонов для всего пакета views
templates = Jinja2Templates(directory="templates")