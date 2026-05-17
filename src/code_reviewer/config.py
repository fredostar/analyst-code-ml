from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    github_token: str = ""
    gitlab_token: str = ""
    mistral_api_key: str = ""
    anthropic_api_key: str = ""

    model_config = SettingsConfigDict(env_prefix="CR_")