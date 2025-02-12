from sqlalchemy.orm import joinedload
from db import get_db
from db.models import *

#Добавление категории в базу данных
def add_category_db(category_name):
    db = next(get_db())
    new_category = GoodsCategory(category_name=category_name)
    db.add(new_category)
    db.commit()
    return True

#Вывод всех товаров в категории
def get_exact_category_db(category_id):
    db = next(get_db())
    category = db.query(GoodsCategory).filter_by(id=category_id).first()
    if category:
        products = db.query(Goods).filter_by(category=category_id).all()
        return {"category": category, "products": products}
    return None

#Вывод всех категорий
def get_all_categories_db():
    db = next(get_db())
    return db.query(GoodsCategory).all()

#Удаление категории
def delete_category_db(categ_id):
    db = next(get_db())
    exact_category = db.query(GoodsCategory).filter_by(id=categ_id).first()
    if exact_category:
        db.delete(exact_category)
        db.commit()
    return False

#Добавление товара в базу данных
def add_product_db(category_id, product_name, price, amount):
    db = next(get_db())
    in_stock = amount > 0
    new_product = Goods(category=category_id, product_name=product_name, price=price, amount=amount, in_stock=in_stock)
    db.add(new_product)
    db.commit()
    return True

#Добавление фотографии товара в базу данных
def add_product_photo_db(photo_file, product_id):
    db = next(get_db())
    new_photo = GoodsPhoto(product_id=product_id, photo_file=photo_file)
    db.add(new_photo)
    db.commit()
    return True

#Вывод одного или всех товаров
def get_product_db(prod_id):
    db = next(get_db())
    if prod_id:
        exact_product = db.query(Goods).options(joinedload(Goods.photos)).filter_by(id=prod_id).first()
        return exact_product if exact_product else False
    return db.query(Goods).options(joinedload(Goods.photos)).all()

#Удаление товара
def delete_product_db(prod_id):
    db = next(get_db())
    exact_product = db.query(Goods).filter_by(id=prod_id).first()
    if exact_product:
        product_photos = db.query(GoodsPhoto).filter_by(product_id=prod_id).all()  # Исправлено на правильный внешний ключ
        for photo in product_photos:
            db.delete(photo)
        db.delete(exact_product)
        db.commit()
        return True
    return False

#Изменение данных товара
def update_product_db(prod_id, field, info):
    db = next(get_db())
    exact_product = db.query(Goods).filter_by(id=prod_id).first()
    if exact_product:
        if field == 'category':
            exact_product.category = info
        elif field == 'product_name':
            exact_product.product_name = info
        elif field == 'price':
            exact_product.price = float(info)
        elif field == 'amount':
            exact_product.amount = int(info)
            # Проверка наличия товара
            exact_product.in_stock = exact_product.amount > 0
        db.commit()
        return True
    return False

#Добавление товара в корзину
def add_to_cart_db(user_id, product_id, quantity):
    db = next(get_db())
    item = db.query(Cart).filter_by(client_id=user_id, goods_id=product_id).first()
    if item:
        # Проверка на наличие выбранного товара в корзине пользователя
        item.quantity += quantity
    else:
        # Если товар не был добавлен ранее, он добавляется в корзину
        product_to_buy = Cart(client_id=user_id, goods_id=product_id, quantity=quantity)
        db.add(product_to_buy)
    db.commit()
    return True

#Вывод корзины клиента
def get_cart_db(user_id):
    db = next(get_db())
    cart = db.query(Cart).filter_by(client_id=user_id).all()
    return cart if cart else []

#Удаление товара из корзины
def delete_in_cart_db(user_id, prod_id):
    db = next(get_db())
    cart_entry = db.query(Cart).filter_by(client_id=user_id, goods_id=prod_id).first()
    if cart_entry:
        db.delete(cart_entry)
        db.commit()
        return True
    return False

#Изменение количества товара в корзине
def update_cart_db(prod_id, user_id, quantity):
    db = next(get_db())
    cart_entry = db.query(Cart).filter_by(client_id=user_id, goods_id=prod_id).first()
    if cart_entry:
        if quantity > 0:
            cart_entry.quantity = quantity
        else:
            # Если изменить количество товара на 0, то он удаляется из корзины
            db.delete(cart_entry)
        db.commit()
        return True
    return False

#Очистка корзины
def clear_cart_db(user_id):
    db = next(get_db())
    cart_items = db.query(Cart).filter_by(client_id=user_id).all()
    if cart_items:
        for item in cart_items:
            db.delete(item)
        db.commit()
        return True
    return False