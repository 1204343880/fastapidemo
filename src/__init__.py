from fastapi import FastAPI
from src.movies.routes import movie_router
from contextlib import asynccontextmanager
# 它是一个协程
from src.db.main import init_db
from src.auth.routes import auth_router

@asynccontextmanager
async def life_span(app: FastAPI):
    # yield 前：应用启动时执行
    print("服务器正在启动")
    await init_db()
    yield  # 从这里开始，FastAPI 开始处理请求
    # yield 后：应用关闭时执行
    print("服务器已停止")


version = "v1"

# lifespan 用于接收的特殊代码
app = FastAPI(
    title="movie api",
    description="一个用于电影网评服务的REST API",
    version=version,
    lifespan=life_span,
)

# 定义端点 所有相关端点都通过这个端点访问
# 这里允许用 f，因为 {version} 是一个已经定义好的 Python 变量：
# tags定义标签类又为了什么？
app.include_router(movie_router,
                   prefix=f"/api/{version}/movies",
                   tags=["movies"]
                   )

app.include_router(auth_router,
                   prefix=f"/api/{version}/auth",
                   tags=["auth"]
                   )