# 和yaml方式有什么区别
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str

    model_config = SettingsConfigDict(
        env_file=".env",
        # 三种不同参数 作用不同
        extra="ignore"
    )


# 建一个配置对象，并把它放进变量 Config
# 配置上面已经创建了 
Config = Settings()
