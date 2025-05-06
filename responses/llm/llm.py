import json
import requests
from config.config import OLLAMA_CONFIG
from models.models import ChatRequest
from utils.ollamaclient import ASYNC_CLIENT, SYNC_CLIENT
from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse
import asyncio
import logging
import httpx
import traceback

logger = logging.getLogger(__name__)

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

    async def event_stream():
        """
        Asynchronous generator function that streams parts of the language model's response.
        Yields the 'content' of each partial message returned by the model client.

        Includes error handling for HTTP issues, timeouts, unexpected response formats,
        and generic exceptions.
        """
        try:
            # Start the streaming request to the language model
            stream = await ASYNC_CLIENT.chat(
                model=request.model,
                messages=request.messages,
                stream=True,
                options=request.options
            )

            # Iterate over the streamed parts and yield their content
            async for part in stream:
                yield part['message']['content']

        except httpx.HTTPError as http_err:
            # Handle HTTP-related errors (e.g., connection issues)
            logger.error(f"HTTP error: {http_err}")
            yield f"Error: HTTP communication failed with the model."

        except asyncio.TimeoutError:
            # Handle request timeout errors
            logger.error("Timeout error during LLM streaming.")
            yield "Error: The request timed out."

        except KeyError as ke:
            # Handle cases where expected keys are missing in the response
            logger.error(f"Key error: {ke}")
            yield "Error: Unexpected response format from the model."

        except Exception as e:
            # Handle any other unexpected exceptions
            print(f"Unexpected error: {e}\n{traceback.format_exc()}")
            logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
            yield "Error: An unexpected error occurred during streaming."

    # Return the event stream as a FastAPI StreamingResponse with appropriate headers
    return StreamingResponse(
        event_stream(),
        media_type="text/plain",
        headers={'Transfer-Encoding': 'chunked'},
        status_code=status.HTTP_202_ACCEPTED
    )

def ollama_model_list():
    """
    Retrieves a list of available model names from the Ollama API server.

    The function makes an HTTP GET request to the configured Ollama socket endpoint (`/api/tags`),
    parses the JSON response to extract model names, and returns them in a JSON response.

    Returns:
        JSONResponse:
            - 200 OK: If models are successfully retrieved.
            - 502 Bad Gateway: If the server response is not valid JSON or another HTTP error occurs.
            - 503 Service Unavailable: If unable to connect to the Ollama server.
            - 504 Gateway Timeout: If the request to the Ollama server times out.
            - 500 Internal Server Error: If unexpected response structure or any other unhandled error occurs.
    """
    try:
        # Attempt to make a GET request to the Ollama server with a 5-second timeout
        request = requests.get(url=OLLAMA_CONFIG['socket'] + '/api/tags', timeout=5)
        request.raise_for_status()  # Raise exception if the response has an error HTTP status

        try:
            # Try decoding and parsing the JSON content from the server
            content = json.loads(request.content.decode('utf8'))
        except json.JSONDecodeError as jde:
            # Handle case where response is not valid JSON
            logger.error(f"Failed to parse JSON response: {jde}")
            return JSONResponse(
                status_code=status.HTTP_502_BAD_GATEWAY,
                content={"detail": "Invalid JSON received from Ollama server."}
            )

        try:
            # Try extracting model names from the 'models' list in the response
            models = [model['name'] for model in content['models']]
        except (KeyError, TypeError) as ke:
            # Handle case where JSON does not have the expected structure
            logger.error(f"Malformed response structure: {ke}")
            return JSONResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                content={"detail": "Unexpected JSON structure from Ollama server."}
            )

        # Return the list of model names with HTTP 200 OK
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"models": models}
        )

    except requests.exceptions.ConnectionError as ce:
        # Handle case where Ollama server is not reachable
        logger.error(f"Connection error: {ce}")
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"detail": "Cannot connect to Ollama server."}
        )

    except requests.exceptions.Timeout:
        # Handle case where request to Ollama server exceeds timeout limit
        logger.error("Timeout while contacting Ollama server.")
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content={"detail": "The request to Ollama server timed out."}
        )

    except requests.exceptions.RequestException as re:
        # Handle any other general request-related exceptions
        logger.error(f"Unhandled request exception: {re}")
        return JSONResponse(
            status_code=status.HTTP_502_BAD_GATEWAY,
            content={"detail": "Unexpected error during HTTP request to Ollama server."}
        )

    except Exception as e:
        # Catch-all for any other unhandled errors
        logger.error(f"Unexpected error: {e}\n{traceback.format_exc()}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "An unexpected error occurred."}
        )
