from fastapi import HTTPException
from fastapi.responses import JSONResponse

from RequestModels.CreatePlanModel import CreatePlanRequest
from TaskHandler.TaskHandler import TaskHandler
from Utility.Utility import getUniqueId
from config import CONFIGURATION, REPORT_ID_CONTEXT


# Set Logging configurations
import logging
logger = logging.getLogger(__name__)


# Setting Up FastAPI app
# -- Used directly by uvicorn/asgi 
from fastapi import FastAPI
app = FastAPI()


# Context Middleware
@app.middleware("http")
async def context_middelware(request, call_next):

    request_id = getUniqueId()
    REPORT_ID_CONTEXT.set(request_id)

    try:
        response = await call_next( request )
    except Exception as error:
        logger.error(f"[-] Request Failed")
        raise HTTPException(
            status = 500,
            detail = "Unable to Serve Request" 
        )
    finally: 
        assert REPORT_ID_CONTEXT.get() == request_id
        logger.debug("[+] Request Ended")
        return response


# Index Endpoint
# -- Could be used to check server heartbeat
@app.get("/")
async def index():
    return { "status" : "success" }


# Plan Get Endpoint
# -- Get Plan / Plan Status for a given plan_id
@app.get("/plan/get/{plan_id}")
async def get_plan(plan_id: str):
    
    raise HTTPException(
        status_code = 503,
        detail = "Endpoint not implemented"
    )


# Plan List Endpoint
# -- List all plans in the system
@app.get("/plan/list")
async def list_reports():
    
    raise HTTPException(
        status_code = 503,
        detail = "Endpoint not implemented"
    )


# Create Plan Endpoint
# -- Create a plan for given information
@app.post("/plan/create")
async def create_plan(request: CreatePlanRequest):

    try:
        endpoint = CONFIGURATION.get("ENDPOINT")
        task_handler = TaskHandler()    
        task_handler.enqueueRequest(
            endpoint = endpoint,
            payload = request.json(),
            task_id = REPORT_ID_CONTEXT.get()   
        )
    except Exception as error:
        logging.error( f"[-] Error : Unable to Enque Task", exc_info = True )
        raise HTTPException (
            status_code = 500,
            detail = "Unable to Enque Task"
        )
        
    return JSONResponse(
        content = { "status" : "success" },
        status_code = 202 
    )
