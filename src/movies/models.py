import uuid
from sqlmodel import SQLModel,Field,Column
#导入 MySQL 方言的专用类型，后面用 mysql.TIMESTAMP。dialects 可以理解为 SQLAlchemy 对不同数据库的适配层。
import sqlalchemy.dialects.mysql as mysql
from sqlalchemy import Uuid
from datetime import datetime,date
from uuid import UUID
# import uuid

# 定义模型类
class Movie(SQLModel,table=True):
    __tablename__ = "movies"
    # Field(...) 则提供这个字段的额外规则。
    uid: UUID = Field(
    # sa_column=...：使用这里定义的 SQLAlchemy 列，而不是让 SQLModel 自动推断列定义。
    # Column(...)：创建数据库列定义。
    # Uuid(as_uuid=True)：数据库按 UUID 类型映射；在 Python 中仍使用 UUID 对象。
    # nullable=False：数据库列不允许为 NULL。
    # primary_key=True：把它设为主键
        sa_column=Column(
            # mysql没有UUID形式   mysql.UUID这个格式是错的
            Uuid(as_uuid=True),
            nullable=False,
            primary_key=True,
            # uuid后的括号()删除 因为会出现每次创建都生成相同uuid的错误
            # uuid4  把函数交过去；每次插入时调用，生成一个新 UUID
            # uuid4()  在立刻调用一次；得到一个 UUID 值，之后可能重复用这个值
            default=uuid.uuid4
        )
    )
    title: str
    director: str
    production_company: str
    release_date: date
    duration_minutes: int
    language: str
    # default_factory=datetime.now：创建 Movie 对象时，自动填入当前时间。
    # nullable=False：数据库不允许它为空
    # 进行优化
    # created_date: datetime = Field(Column(mysql.TIMESTAMP,default=datetime.now))
    # update_date: datetime = Field(Column(mysql.TIMESTAMP,default=datetime.now))
    # sa_column是SQLModel的Field(...)提供的参数
    created_date: datetime = Field(sa_column=Column(mysql.TIMESTAMP,default=datetime.now))
    update_date: datetime = Field(sa_column=Column(mysql.TIMESTAMP,default=datetime.now))
#__repr__ 是 Python 的特殊方法，用来定义对象“显示出来是什么样”
def __repr__(self):
    return f"<Movie ({self.title})>"