from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    KAFKA_BOOTSTRAP_SERVER: str = "localhost:9095,localhost:9097,localhost:9102"
    KAFKA_TOPIC_POSTS: str = "posts"
    KAFKA_CONSUMER_GROUP: str = "posts-group"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )

Config = Settings()

broker_connection_retry_on_startup = True