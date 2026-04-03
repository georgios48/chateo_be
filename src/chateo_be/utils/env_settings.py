import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_env_var(key: str, required: bool = False) -> str:
    val = os.getenv(key)
    if required and not val or val is None:
        raise ValueError(f"Missing required environment variable: {key}")
    return val


@dataclass
class EnvConfig:
    """
    Environment configuration for API integration.
    This class retrieves configuration values from environment variables,
    providing defaults and validation as needed.
    """

    # Environment
    environment: str = field(default_factory=lambda: get_env_var("ENVIRONMENT", required=True))
