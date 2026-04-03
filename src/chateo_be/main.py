from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.chateo_be.utils.env_settings import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager to handle startup and shutdown events.
    """

    # On Start

    yield

    # On Shutdown

# Load environment configuration
config = get_settings()

# Set debug if it is dev/local
debug = config.environment.lower() in {"dev", "local"}

# Initialize the FastAPI application
app = FastAPI(lifespan=lifespan, debug=debug)

# Configure Middleware and origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints
