# 服务文件 专门实现逻辑的地方

from .models import  User
from  .schemas import UserCreateModel
from .utils import generate_password_hash
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

class UserService:
    # 这直接用user是没数据的吧    这self是啥老是忘  self是当前 UserService 实例本身
    async def get_user_by_email(self,email: str, session:AsyncSession):
        statement = select(User).where(User.email == email)
        # 这个地方是真正去数据库执行的地方？
        result = await session.execute(statement)
        user = result.scalars().first()
        return user
    # 使用这个方法检查用户是否存在
    async def user_exists(self,email: str, session:AsyncSession):
        user = await self.get_user_by_email(email, session)
        # if user is None:
        #     return False
        # else:
        #     return True

        # 三元语句
        return True if user is not None else False

    async def create_user(self,user_data:UserCreateModel, session:AsyncSession):
        user_data_dict = user_data.model_dump()
        new_user = User(
            **user_data_dict,
        )
        new_user.password_hash = generate_password_hash(user_data_dict['password'])
        session.add(new_user)
        await session.commit()

        return new_user