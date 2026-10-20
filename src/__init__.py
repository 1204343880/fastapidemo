from fastapi import FastAPI

from src.movies.routes import movie_router


version = "v1"

app = FastAPI(
    title="Movie API - in-memory practice",
    description="使用 Python 列表练习 CRUD；不连接数据库。",
    version=version,
)

app.include_router(
    movie_router,
    prefix=f"/api/{version}/movies",
    tags=["movies"],
)
