from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "wellness-profile-api"
    database_url: str = "mysql+pymysql://root:1234@localhost:3306/wellness?charset=utf8mb4"
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
