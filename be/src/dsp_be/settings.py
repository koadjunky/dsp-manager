from environs import Env

env = Env()
env.read_env()  # read .env file, if it exists

APP_SETTINGS = {
    "title": "DSP manager backend",
    "description": "Application for managing factories in Dyson Sphere Program",
    "docs_url": None,
    "redoc_url": None,
}
API_PREFIX = ""

DEFAULT_HOST = env.str("DEFAULT_HOST", "localhost")
DEFAULT_HOST_PORT = env.int("DEFAULT_HOST_PORT", 8001)
