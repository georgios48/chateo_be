import os
from dataclasses import dataclass, field
from functools import lru_cache

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_var(
    key: str, required: bool = False, *, aliases: tuple[str, ...] = ()
) -> str:
    val = os.getenv(key)
    if not val:
        for alt in aliases:
            val = os.getenv(alt)
            if val:
                break
    if required and not val:
        raise ValueError(f"Missing required environment variable: {key}")
    return val or ""


@dataclass
class EnvConfig:
    """
    Environment configuration for API integration.
    This class retrieves configuration values from environment variables,
    providing defaults and validation as needed.
    """

    # Environment
    environment: str = field(
        default_factory=lambda: get_env_var(
            "ENVIRONMENT", required=True, aliases=("environment",)
        )
    )

    # Database URL
    database_url: str = field(default_factory=lambda: get_env_var("DATABASE_URL", required=True))

    # CORS (comma-separated); default allows all for local dev
    allowed_origins: tuple[str, ...] = field(
        default_factory=lambda: tuple(
            x.strip()
            for x in get_env_var("ALLOWED_ORIGINS", required=False).split(",")
            if x.strip()
        )
        or ("*",)
    )


@lru_cache
def get_settings():
    """
    Returns the environment configuration.
    """
    return EnvConfig()
