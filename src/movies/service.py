# 增删改查逻辑全在这 通过一个类实现
from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import MovieCreateModel, MovieUpdateModel
# 错误原因  from sqlalchemy import select, desc
from sqlmodel import select, desc
from .models import Movie
from datetime import datetime
from uuid import UUID


class Service:
    # 接收self 通过book service对象访问方法
    # session 帮助对数据库执行任意类型增删改查
    # 获取全部电影列表
    # session: AsyncSession：声明这个方法需要一个异步数据库会话。这只是类型标注，不会自动创建或传入 session。
    async def get_all_movie(self, session: AsyncSession):
        statement = select(Movie).order_by(desc(Movie.created_date))
        # await session.exec(statement)：把查询发送到数据库，并等待结果返回
        result = await session.exec(statement)
        # 把查询结果中的全部电影取出来，作为列表返回。
        return result.all()

    # 通过uid 根据uid查询电影
    async def get_movie(self, movie_uid: UUID, session: AsyncSession):
        statement = select(Movie).where(Movie.uid == movie_uid)
        result = await session.exec(statement)
        movie = result.first()
        if movie is not None:
            return movie
        else:
            return None

    # 创建电影
    async def create_movie(self, movie_data: MovieCreateModel, session: AsyncSession):
        movie_data_dict = movie_data.model_dump()
        new_movie = Movie(**movie_data_dict)
        new_movie.release_date = datetime.strptime(movie_data_dict['release_date'], '%Y-%m-%d').date()
        session.add(new_movie)
        await session.commit()
        return new_movie

    # 更新电影信息
    async def update_movie(self, movie_uid: str, update_data: MovieUpdateModel, session: AsyncSession):
        movie_to_update = await self.get_movie(movie_uid, session)
        if movie_to_update is None:
            return None
        update_data_dict = update_data.model_dump()
        update_data_dict["release_date"] = datetime.strptime(
            update_data_dict["release_date"], "%Y-%m-%d"
        ).date()

        for key, value in update_data_dict.items():
            setattr(movie_to_update, key, value)

        await session.commit()
        return movie_to_update


    # 根据id 删除电影
    async def delete_movie(self, movie_uid: str, session: AsyncSession):
        movie_to_delete = await self.get_movie(movie_uid, session)
        if movie_to_delete is not None:
            await session.delete(movie_to_delete)
            await session.commit()
            return {}
        else:
            return None
