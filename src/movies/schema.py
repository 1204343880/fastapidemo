from pydantic import BaseModel
import uuid
from datetime import datetime, date


# 后面不要带,
# 创建名为 Movie 的 Pydantic 模型。BaseModel 提供字段检查能力。
# 这里定义的是数据结构
class Movie(BaseModel):
    uid: uuid.UUID
    title: str
    director: str
    production_company: str
    release_date: str
    duration_minutes: int
    language: str
    created_date: datetime
    update_date: datetime


class MovieCreateModel(BaseModel):
    uid: uuid.UUID
    title: str
    director: str


class MovieUpdateModel(BaseModel):
    title: str
    director: str
    production_company: str
    release_date: str
    duration_minutes: int
    language: str
