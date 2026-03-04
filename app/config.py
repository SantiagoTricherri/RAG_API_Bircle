from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "RAG API"
    openai_api_key: str
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    collection_name: str = "documents"
    api_key: str = "supersecret"

    class Config:
        env_file = ".env"


settings = Settings()