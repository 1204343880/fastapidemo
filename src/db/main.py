# 再用yaml方式实现一次   还有于pymysql实现方式的区别
# 之前：YAML → 程序读取配置 → PyMySQL → MySQL
# 当前：.env → Settings → SQLAlchemy AsyncEngine → asyncmy → MySQL
from markdown_it.rules_inline import text
# asyncmy:让 Python 能异步连接 MySQL 的驱动
# sqlmodel:在 SQLAlchemy 和 Pydantic 基础上，提供更方便的模型定义
from sqlmodel import create_engine, SQLModel
# Q:这个又是什么？  为什么sqlalchemy可以直接用
# SQLAlchemy：负责 Engine、连接、Session、ORM 等数据库操作机制。
# A:SQLModel 建立在 SQLAlchemy 之上，所以会作为依赖一起安装。
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from src.movies.models import Movie
from src.config import Config

# 异步与同步 用一个清晰概念解释我都讲不清了？？？
# 同步是排队等一个操作完成，再做下一个
# 异步是在等网络、数据库等 I/O 结果时，先去处理别的任务。

# AsyncEngine异步引擎对象
# create_async_engine 会创建异步 Engine

# 异步引擎
# engine = AsyncEngine(
#     create_async_engine(
#         url=Config.DATABASE_URL,
#         # 建一个配置对象，并把它放进变量 Config
#         echo=True,
#     ))
engine = create_async_engine(
    Config.DATABASE_URL,
    echo=True,
)


async def init_db():
    async with engine.begin() as conn:
        # 创建并访问元数据
        await conn.run_sync(SQLModel.metadata.create_all)


# 创建一个session 共享资源
# 使用sqlmodel异步session  感觉这种异步上是么都
async def get_session() -> AsyncSession:
    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with Session() as session:
        yield session
