from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from src.movies.service import Service
from src.movies.schemas import  Movie,MovieCreateModel,MovieUpdateModel
from src.db.main import get_session
from typing import List
from uuid import UUID

# 路由器来将相关api端点进行分组
movie_router = APIRouter()

movie_service = Service()


# 坏了 给我看的有些宕机了
# 查看电影列表
# response_model什么意思
# response_model 描述的是响应正文的数据结构 返回应该是一个电影列表

# 为什么后面写个类？返回状态吗是   response_model=List[Movie])
# 这个接口返回电影列表，每一项都要符合 Movie 的字段和类型。
# 这样 FastAPI 可以校验响应、生成接口文档，并按模型处理返回数据。

# 如果没有电影，List[Movie] 接口返回空列表 []，结构还符合吗？
# [] 符合 List[Movie]。它是一个列表，只是里面暂时没有电影；没有元素违反 Movie 结构，所以响应校验通过。
@movie_router.get("/", response_model=List[Movie])
# 这样写反而是错的 这是为什么 这个传的是什么？
#  这种格式才对/movies?movies=...
# async def read_movies(movies):
#     return movies
# session: AsyncSession：标明 session 应该是异步数据库会话
# Depends(get_session)：告诉 FastAPI 通过依赖函数 get_session 提供这个参数
# 语法不熟练！！！
async def get_all_movies(session: AsyncSession = Depends(get_session)):
    # 都是协程中定义的方法 要await调用
    movies = await movie_service.get_all_movie(session)
    return movies


# 根据uid 查找电影
@movie_router.get("/{movie_uid}")
async def get_movie(movie_uid:UUID,session: AsyncSession = Depends(get_session)):
    movie = await movie_service.get_movie(movie_uid,session)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
               detail="Movie not found")

    # 这一行为什么这样写？  return movie.model_dump()
    # 把数据库模型对象转换成字典
    #  第二种解决方案就是把本身get-movie返回字典的要求改掉
    return movie

# 增加新电影
@movie_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Movie)
async def create_movies(
        movie_data: MovieCreateModel, session: AsyncSession = Depends(get_session)) -> dict:
    new_movie = await movie_service.create_movie(movie_data, session)
    # # model_dump方法可以将数据转化为列表中的字典
    # # model_dump() 把 Pydantic 的 Movie 模型对象转换成一个 Python 字典
    # new_movie = movie_data.model_dump()
    # movie_data: MovieCreateModel    # movie_routerend方法就是追加到列表末尾 只适用于列表
    # movies.movie_routerend(new_movie)
    return new_movie


# 修改电影数据
@movie_router.patch("/{movie_uid}")
async def update_movies(movie_uid: UUID, movie_update_data: MovieUpdateModel,
                        session: AsyncSession = Depends(get_session)) -> dict:
    updated_movie = await movie_service.update_movie(movie_uid, movie_update_data, session)

    # 这里没看懂 为什么里面还调用函数自己 还是我写错代码了
    if updated_movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")
    return updated_movie.model_dump()

# 删除电影
# 加上 f 后，Python 会先把大括号里的内容当作 Python 表达式计算，再把结果交给 FastAPI
# f "/movies/{movie_id}"  这格式完全错误
@movie_router.delete("/{movie_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_movies(movie_uid: UUID, session: AsyncSession = Depends(get_session)) -> None:
    # 为什么uid要统一，什么原因？？
    movie_to_delete = await movie_service.delete_movie(movie_uid, session)

    if movie_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Movie not found")

    return None
