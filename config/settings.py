from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    DEV = "dev"
    PROD = "prod"
    STAGING = "staging"


class Settings(BaseSettings):
    """Application settings and configuration.

    Attributes:
        debug: Debug mode flag
        environment: Current environment (dev/prod/staging)
        app_name: Name of the application
        deepseek_api_key: API KEY for DEEPSEEK platform
        project_path: Base path of the project
        hf_token: Hugging Face API token
        openai_api_key: OpenAI API key
    """

    debug: bool = Field(default=False, description="Debug mode flag")
    environment: Environment = Field(
        default=Environment.DEV, description="Current environment (dev/prod/staging)"
    )
    app_name: str = Field(default="AgentsCourse", description="Name of the application")
    deepseek_api_key: str = Field(
        description="API KEY for DEEPSEEK platform", validation_alias="DEEPSEEK_API_KEY"
    )
    open_api_key: str = Field(
        description="API KEY for OPENAI platform", validation_alias="OPENAI_API_KEY"
    )
    project_path: Path = Field(
        default=Path(__file__).parent.parent, description="Base path of the project"
    )
    hf_token: str = Field(description="Hugging Face API token", validation_alias="HF_TOKEN")

    serper_api_key: str = Field(description="Serper API KEY", validation_alias="SERPER_API_KEY")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, env_prefix="myapp_"
    )

    def model_dump(self) -> dict[str, Any]:
        """Override model_dump to include computed values if needed."""
        return super().model_dump()


settings = Settings()

if __name__ == "__main__":
    print(settings.model_dump())
