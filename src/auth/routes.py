from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import UserCreateModel, UserModel,UserloginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException
from .utils import create_access_token,decode_token,verify_password
from datetime import timedelta


auth_router = APIRouter()
user_services = UserService()

REFRESH_TOKEN_EXPIRY = 2



#注册路由
@auth_router.post("/signup",
                  response_model=UserModel,
                  status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreateModel,
                      session: AsyncSession = Depends(get_session)):
    email = user_data.email
    # 协程 所以必须是await
    user_exists = await user_services.user_exists(email, session)

    if user_exists:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail="具有该邮箱的用户已存在")
    new_user = await user_services.create_user(user_data, session)
    return new_user

@auth_router.post("/login",)
# session: AsyncSession = Depends(get_session) 的作用是：
# 让 FastAPI 在处理这次请求时，准备一个异步数据库会话，并传给路由函数。
async def login_user(user_login_data:UserloginModel,session: AsyncSession = Depends(get_session)):
        email = user_login_data.email
        password = user_login_data.password

        # 拿到 session 后，路由就能把它传给 Service
        user = await user_services.get_user_by_email(email, session)

        if user is not None:
            password_valid = verify_password(password, user.password_hash)

            if password_valid:
                # 登录令牌
                access_token = create_access_token(
                    user_data={
                        "email": user.email,
                        "user_uid" : str(user.uid),
                    }
                )

                # 刷新令牌
                # 这个是因为参数的不同吗？   传true就是刷新令牌
                refresh_token = create_access_token(
                    user_data={
                        "email": user.email,
                        "user_uid" : str(user.uid),
                    },
                    refresh=True,
                    expiry = timedelta(days=REFRESH_TOKEN_EXPIRY)
                )
                # 这个是为了控制json返回的具体形式是么？
                return JSONResponse(
                    content={
                        "message": "Login Successful",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user":{
                            "email": user.email,
                            "uid": str(user.uid),
                        }
                    },
                )

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="请检查邮箱或者密码")