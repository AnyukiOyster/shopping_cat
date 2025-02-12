from datetime import datetime
from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db import Base

## Модель для клиентов
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=True)
    tel = Column(String, nullable=False)
    reg_date = Column(DateTime, default=datetime.now())

## Модели для товаров
# Список категорий товаров
class GoodsCategory(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String, nullable=False)

# Список товаров
class Goods(Base):
    __tablename__ = "goods"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(String, ForeignKey("category.id"))
    product_name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    amount = Column(Integer, nullable=False)
    in_stock = Column(Boolean, default=True)

    category_fk = relationship(GoodsCategory, lazy='subquery')

# Фотографии товаров
class GoodsPhoto(Base):
    __tablename__ = "goods_photos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('goods.id'))
    photo_file = Column(String, nullable=False)

    goods_fk = relationship(Goods, lazy='subquery')
    photos = relationship('GoodsPhoto', backref='product', lazy='subquery')

## Модель для корзины
class Cart(Base):
    __tablename__ = "user_cart"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("clients.id"))
    goods_id = Column(Integer, ForeignKey("goods.id"))
    quantity = Column(Integer, nullable=False)

    client_fk = relationship(Client, lazy='subquery')
    goods_fk = relationship(Goods, lazy='subquery')