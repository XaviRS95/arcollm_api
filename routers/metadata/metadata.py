from fastapi import APIRouter, status, Request
from fastapi.responses import JSONResponse
from config.config import API_CONFIG
#from utils.decorators import execution_handler
metadata_router = APIRouter()

@metadata_router.get('/api/metadata')
async def get_metadata():

    return JSONResponse(
        content = {
            'name':API_CONFIG['name'],
            'environment': API_CONFIG['environment'],
            'version':API_CONFIG['version']},
        status_code = status.HTTP_200_OK)