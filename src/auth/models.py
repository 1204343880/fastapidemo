import uuid
from datetime import datetime
import sqlalchemy.dialects.mysql as mysql
from sqlmodel import SQLModel,Field,Column
from sqlalchemy import Uuid


# 定义users表与 Python User对象的映射，供建表和用户数据的增删改查使用
class User(SQLModel, table=True):
    __tablename__ = "users"
    uid: uuid.UUID = Field(sa_column=Column(
            Uuid(as_uuid=True),
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        ))
    username: str
    email: str
    first_name: str
    last_name: str
    is_verified: bool = Field(default=False)
    created_date: datetime = Field(sa_column=Column(mysql.TIMESTAMP,default=datetime.now))
    update_date: datetime = Field(sa_column=Column(mysql.TIMESTAMP,default=datetime.now))

    # self：当前这个用户对象，例如上面的 user
    # __repr__ 的具体用途是：让你查看对象时，得到容易辨认的文字，方便调试
    def __repr__(self):
        return f"<User {self.username}>"