from config.config import OLLAMA_CONFIG
from ollama import AsyncClient, Client


SYNC_CLIENT = Client(
    host = OLLAMA_CONFIG['socket']
)

ASYNC_CLIENT = AsyncClient(
    host = OLLAMA_CONFIG['socket']
    )

