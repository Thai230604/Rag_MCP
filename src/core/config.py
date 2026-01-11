from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # OpenAI
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    
    # Qdrant
    qdrant_host: str = "localhost"
    qdrant_port: int = 6333
    qdrant_api_key: str = "your-secret-key"
    qdrant_collection: str = "documents"
    
    # Embedding
    embedding_model: str = "text-embedding-3-small"
    embedding_dim: int = 1536
    
    # Application
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
