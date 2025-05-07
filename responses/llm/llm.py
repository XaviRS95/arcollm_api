import json
import requests
from config.config import OLLAMA_CONFIG
from models.models import ChatRequest
from utils.ollamaclient import ASYNC_CLIENT, SYNC_CLIENT
from fastapi import status
from starlette.responses import StreamingResponse, JSONResponse
import asyncio
import logging
import httpx
import traceback


async def async_chat_request(request: ChatRequest):
    """
    Handles a streaming chat request using an asynchronous language model client.

    Args:
        request (ChatRequest): The incoming chat request containing the model name,
                               message history, and additional options.

    Returns:
        StreamingResponse: A FastAPI streaming response that yields partial responses
                           from the language model in real time with appropriate headers.
    """
    if request.messages is None:
        return JSONResponse(
            content= {"detail": "No message from user was sent"},
            media_type="application/json",
            status_code = status.HTTP_400_BAD_REQUEST
        )

    async def event_stream():
        """
        Asynchronous generator function that streams parts of the language model's response.
        Yields the 'content' of each partial message returned by the model client.

        Includes error handling for HTTP issues, timeouts, unexpected response formats,
        and generic exceptions.
        """
        stream = await ASYNC_CLIENT.chat(
            model=request.model,
            messages=request.messages,
            stream=True,
            options=request.options
        )
        # Iterate over the streamed parts and yield their content
        async for part in stream:
            yield part['message']['content']

    # Return the event stream as a FastAPI StreamingResponse with appropriate headers
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={'Transfer-Encoding': 'chunked'},
        status_code=status.HTTP_202_ACCEPTED
    )

def sync_chat_request(request: ChatRequest):
    """
    Process a synchronous chat completion request using the SYNC_CLIENT.

    This function takes a `ChatRequest` object containing the model name, message history,
    and optional parameters. It then forwards the request to the synchronous language model client
    and returns the generated message content as a JSON response.

    Args:
        request (ChatRequest): Object containing the model to use, a list of messages
                               (history), and any additional client-specific options.

    Returns:
        JSONResponse: HTTP response with status code 200 and the generated message content
                      from the language model in the format:
                      {
                          "message": <string>
                      }
    """
    # Generate chat completion using the synchronous client
    response = SYNC_CLIENT.chat(
        model=request.model,
        messages=request.messages,
        stream=False,
        options=request.options
    )

    # Return the generated message content in a standardized JSON format
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": response['message']['content']}
    )


def ollama_model_list():
    """
    Retrieve the list of available models from the Ollama server.

    This function sends a GET request to the Ollama server's `/api/tags` endpoint
    to fetch available model tags. If the request is successful, it extracts the model
    names from the response and returns them in a JSON response.

    Raises:
        requests.exceptions.RequestException: If the HTTP request to the Ollama server fails.

    Returns:
        JSONResponse: HTTP response with status code 200 and a list of model names
                      in the format:
                      {
                          "models": [<model_name1>, <model_name2>, ...]
                      }
    """
    # Send GET request to Ollama's /api/tags endpoint with a 5-second timeout
    request = requests.get(url=OLLAMA_CONFIG['socket'] + '/api/tags', timeout=5)

    # Raise exception if the HTTP request failed (e.g., 4xx or 5xx status code)
    request.raise_for_status()

    # Parse response content from JSON
    content = json.loads(request.content.decode('utf8'))

    # Extract list of model names from the response
    models = [model['name'] for model in content['models']]

    # Return list of models in JSON response
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"models": models}
    )