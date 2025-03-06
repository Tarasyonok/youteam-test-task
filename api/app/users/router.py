from fastapi import APIRouter, Depends, Response

from app.exceptions import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import create_access_token, get_password_hash, authenticate_user
from app.users.dao import UserDAO
from app.users.dependencies import get_current_user
from app.users.models import User
from app.users.schemas import SUserLogin, SUserRegister

auth_router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@auth_router.post("/register")
async def register_user(response: Response, user_data: SUserRegister):
    existing_user = await UserDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    user_id = await UserDAO.add(email=user_data.email, hashed_password=hashed_password, name=user_data.name)
    print("!" * 20)
    print(user_id)
    print("!" * 20)
    access_token = create_access_token({"sub": str(user_id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@auth_router.post("/login")
async def login_user(response: Response, user_data: SUserLogin):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@auth_router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


users_router = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@users_router.get("/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user


@users_router.get("")
async def read_users_all():
    return await UserDAO.find_all()