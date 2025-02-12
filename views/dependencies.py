from db.shopservice import get_all_categories_db

# Функция-зависимость для получения категорий
def get_categories():
    categories = get_all_categories_db()
    return {"categories": categories}