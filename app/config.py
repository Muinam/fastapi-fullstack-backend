from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

_base_config = SettingsConfigDict(
    env_file=".env",
    env_ignore_empty=True,
    extra="ignore"
)

class securitySetting(BaseSettings):
    model_config = _base_config
    JWT_SECRET_KEY :str
    JWT_ALGORITHM:str


security_settings = securitySetting()