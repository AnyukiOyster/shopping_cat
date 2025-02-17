from db.shopservice import get_all_categories_db
from views.user_auth import get_current_user, User
from fastapi import Depends

# Функция-зависимость для получения категорий
async def get_categories():
    categories = get_all_categories_db()
    user = None
    try:
        user = await get_current_user()
    except:
        pass
    return {"categories": categories, "user": user}

# Получение айди текущего пользователя
def show_current_user_id(user: User = Depends(get_current_user)) -> int:
    return user.id