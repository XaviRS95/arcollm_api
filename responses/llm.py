import json
import requests
from config.config import OLLAMA_CONFIG
from utils.ollamaclient import ASYNC_CLIENT, SYNC_CLIENT

async def ollama_async_client_request(messages: list, model: str):
    async for part in await ASYNC_CLIENT.chat(
            model=model,
            messages=messages,
            stream=True,
            options={}
    ):
        yield part['message']['content']


def ollama_sync_client_request(message: str, model: str):
    message = {'role': 'user', 'content': message}
    response = SYNC_CLIENT.chat(
        model=model,
        messages=[message]
    )
    return response['message']['content']

async def ollama_model_list():
    request = requests.get(url=OLLAMA_CONFIG['socket']+'/api/tags')
    content = request.content
    decode = content.decode('utf8')
    content = json.loads(decode)
    models = []
    for model in content['models']:
        models.append(model['name'])
    return models