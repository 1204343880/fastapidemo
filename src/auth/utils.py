# 认证相关实用函数
from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt

password_context = CryptContext(
    schemes=["bcrypt"])

def generate_password_hash(password: str):
    hash = password_context.hash(password)
    return hash

# 这一页到现在我都没手打几个 全是自己出来的 这补全有点厉害了
def verify_password(password:str, hash:str):
    return password_context.verify(password, hash)

def create_access_token(user_data: dict, expires: timedelta):
    payload = {}

    token = jwt.encode(
        payload=user_data,
        key=22
    )