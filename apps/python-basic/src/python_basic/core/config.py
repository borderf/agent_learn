from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    openai_api_key: str
    openai_base_url: str = "https://api.deepseek.com"
    default_model: str = "deepseek-v4-flash"
    database_url = "mysql://root:123456@localhost:3306/ai_agent"


settings = Settings()
