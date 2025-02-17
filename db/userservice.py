from db import get_db
from db.models import Client

#Добавление пользователя в базу данных
def add_user_db(name, tel, password, surname= None):
    db = next(get_db())
    new_client = Client(name=name, tel=tel, password=password, surname= surname)
    db.add(new_client)
    db.commit()
    return True

#Вывод данных о пользователе
def get_exact_user_db(user_id):
    db = next(get_db())
    exact_user = db.query(Client).filter_by(id=user_id).first()
    if exact_user:
        return exact_user
    return False

def get_user_id_by_tel(tel):
    db = next(get_db())
    user = db.query(Client.id).filter(Client.tel == tel).first()
    return user.id if user else None

#Удаление пользователя
def delete_user_db(user_id):
    db = next(get_db())
    exact_user = db.query(Client).filter_by(id=user_id).first()
    if exact_user:
        db.delete(exact_user)
        db.commit()
    return False

#Изменение данных пользователя
def update_user_db(user_id, field, info):
    db = next(get_db())
    exact_user = db.query(Client).filter_by(id=user_id).first()
    if exact_user:
        if field == 'name':
            exact_user.name = info
        elif field == 'surname':
            exact_user.surname = info
        elif field == 'tel':
            exact_user.tel = info
        elif field == 'password':
            exact_user.password = info
        db.commit()
        return True
    return False