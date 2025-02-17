from fastapi import Request, Depends, HTTPException, Form, status, APIRouter
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Optional
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from config import algorithm, access_token_exp_minutes, secret_key
from datetime import datetime, timedelta
from db.models import Client
from pydantic import BaseModel
from db.userservice import *
from jose import JWTError, jwt
from db import get_db
from sqlalchemy.orm import Session
from views import templates

router = APIRouter()

@router.get("/registration", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)

@router.post("/registration")
async def register_user(request: Request, tel: str = Form(...), password: str = Form(...), name: str = Form(...), surname: str = Form(None), db: Session = Depends(get_db)):
    existing_user = db.query(Client).filter(Client.tel == tel).first()
    if existing_user:
        return templates.TemplateResponse("register.html", request=request, context={"error": "Этот номер телефона уже зарегистрирован."})
    add_user_db(name=name, tel=tel, password=password, surname=surname)
    return RedirectResponse(url="/login", status_code=303)

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    tel: str

class UserAuth(BaseModel):
    tel: str
    hashed_password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# Функция для проверки пароля
def verify_password(password, hashed_password):
    """
    :param password: Пароль, который ввел пользователь
    :param hashed_password: Пароль в бд
    :return:
    """
    return password == hashed_password

# Функция получения пользователя из БД
def get_user(db: Session, tel: str):
    return db.query(Client).filter(Client.tel == tel).first()

# Функция для создания токена
def create_access_token(data, expire_date: Optional[timedelta] = None):
    to_encode = data.copy()
    if expire_date:
        expire = datetime.utcnow() + expire_date
    else:
        expire = datetime.utcnow() + timedelta(minutes=access_token_exp_minutes)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, secret_key, algorithm=algorithm)
    return encoded_jwt

# Авторизация и получение токена (API)
@router.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Неверное имя пользователя или пароль")
    access_token = create_access_token(data={"sub": user.tel})
    return {"access_token": access_token, "token_type": "bearer"}

# Функция для проверки текущего пользователя
async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Ошибка авторизации")
    print(token)
    try:
        payload = jwt.decode(token, secret_key, algorithms=[algorithm])
        tel: str = payload.get("sub")
        if tel is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(db, tel)
    if user is None:
        raise credentials_exception
    return User(id=user.id, tel=user.tel)

# Получение информации о текущем пользователе
@router.get("/user/me", response_model=User)
async def user_me(user: User = Depends(get_current_user)):
    return user

# Авторизация и получение токена (HTML)
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_user(request: Request, tel: str = Form(...), password: str = Form(...)):
    #Вывод ID пользователя по телефону
    user_id = get_user_id_by_tel(tel)
    if not user_id:
        return templates.TemplateResponse("login.html", request=request, context={"error": "Пользователь не найден"})
    user = get_exact_user_db(user_id)
    if not user or user.password != password:
        return templates.TemplateResponse("login.html", request=request, context={"error": "Неверный номер телефона или пароль"})
    # Создание токена
    access_token = create_access_token(data={"sub": user.tel})
    response = RedirectResponse("/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    print(access_token)

    return response