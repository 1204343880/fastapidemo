from fastapi import APIRouter, Depends, HTTPException, status
from .schemas import UserCreateModel, UserModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio.session import AsyncSession
from fastapi.exceptions import HTTPException

auth_router = APIRouter()
user_services = UserService()


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
