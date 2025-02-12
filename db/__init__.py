from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Тип базы данных (sqlite)
SQL_DATABASE_URI = "sqlite:///catshop.db"

# Создаем движок
engine = create_engine(SQL_DATABASE_URI)

# Создаем сессию для хранения данных
SessionLocal = sessionmaker(bind=engine)

# Создаем базу данных
Base = declarative_base()

# Функция для подключения к бд
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()