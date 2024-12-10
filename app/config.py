from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    OPENAI_API_KEY: str
    database_host: str
    database_port: int
    database_name: str
    database_username: str
    database_password: str

    @property
    def database_url(self):
        return f"postgresql://{self.database_username}:{self.database_password}@{self.database_host}:{self.database_port}/{self.database_name}"

    class Config:
        env_file = ".env"


settings = Settings()