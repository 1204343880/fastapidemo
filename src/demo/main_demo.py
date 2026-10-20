# 实例类导入
from fastapi import FastAPI, Header
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


# 路径参数-传递变量
@app.get("/greet1/{name}")
# Q:那如果变成 age,name 还能正确匹配吗
# A:参数顺序不决定来源，参数名和路由声明决定来源。
# 这个地方的name是路径参数  而且上下必须一致只能是name
async def greet_name1(name: str) -> dict:
    return {"message": f"Hello, {name}!"}


@app.get("/greet2/")
# 这个地方的name是路径参数  而且上下必须一致只能是name
# 且这里面的name是查询参数 也就是?name=xxx
async def greet_name1(name: str) -> dict:
    return {"message": f"Hello, {name}!"}


# 混合使用路径和查询参数   greet1和2的结合
@app.get("/greet3/{name}")
# 这个地方的name是路径参数  而且上下必须一致只能是name
async def greet_name1(name: str, age: int) -> dict:
    # Q: 这个age为什么不报错  和name不一样的机制？
    # A: 因为age是一个查询参数，而不是路径参数。
    # 路径参数是通过URL路径传递的，而查询参数是通过URL的查询字符串传递的
    # http://127.0.0.1:8000/greet3/yuyu?age=21
    return {"message": f"Hello, {name}", "age": age}


# 如何使用路径和恶查询参数向服务器传递数据
@app.get("/greet4")
# name和age都得有默认值 
async def greet_name1(name: Optional[str] = "User", age: int = 0) -> dict:
    return {"message": f"Hello, {name}", "age": age}


class MovieCreateModel(BaseModel):
    title: str  # 标题
    author: str  # 作者


# 传输数据
@app.post("/create_movie")
# 路径处理函数 当作参数处理
async def create_movie(movie_data: MovieCreateModel):
    return {
        "title": movie_data.title,
        "author": movie_data.author,
    }


# fastapi创建简单网络服务器的方法
@app.get("/get_headers")
async def get_headers(
        accept: str = Header(None),
        content: str = Header(None),
        # 关于大小写 请求头 请求体的一些东西
        content_type: str = Header(None),
        user_agent: str = Header(None),
        host: str = Header(None),
):
    request_headers = {
        "Accept": accept,
        "Content": content,
        "Content_type": content_type,
        "User_Agent": user_agent,
        "Host": host,
    }

    return request_headers
