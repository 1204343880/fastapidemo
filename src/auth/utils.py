# 认证相关实用函数
from passlib.context import CryptContext
from datetime import datetime, timedelta
from src.config import Config
import jwt
import uuid
import logging

password_context = CryptContext(
    schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 1800

def generate_password_hash(password: str):
    hash = password_context.hash(password)
    return hash

# 这一页到现在我都没手打几个 全是自己出来的 这补全有点厉害了
def verify_password(password:str, hash:str):
    return password_context.verify(password, hash)


# 创建登录令牌
def create_access_token(user_data: dict, expiry: timedelta = None,refresh:bool = False):
    payload = {}

    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())
    payload['refresh'] = refresh

    token = jwt.encode(
        # 令牌要携带数据
        payload=payload,
        key=Config.JWT_SECRET,
        # 签名算法
        algorithm=Config.JWT_ALGORITHM
    )

    return token

def decode_token(token: str) -> dict:
    try:
        token_data = jwt.decode(
            token = token,
            key=Config.JWT_SECRET,
            # algorithms 表示服务端允许接受的算法列表。即使只允许 "HS256" 一种，也要把它放进列表
            algorithms=[Config.JWT_ALGORITHM])
        return token_data

    except jwt.PyJWTError as e:
        logging.exception(e)
