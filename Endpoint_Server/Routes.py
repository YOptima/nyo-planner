from Utility.Utility import getUniqueId
from fastapi import FastAPI, HTTPException
app = FastAPI()

from RequestModels.CreatePlanModel import CreatePlanRequest
from TaskHandler.TaskHandler import TaskHandler
from config import CONFIGURATION
from Logging.Filters import ContextFilter

# Set Logging configurations
import logging
import logging.config
from config import LOGGING_CONFIGURATION
logging.config.dictConfig(LOGGING_CONFIGURATION)
logger = logging.getLogger(__name__)

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
    
    endpoint = CONFIGURATION.get("ENDPOINT")
    report_id = getUniqueId()

    logging_filter = ContextFilter(report_id)
    logger.addFilter(logging_filter)

    try:
        task_handler = TaskHandler()    
        task_handler.enqueueRequest(
            endpoint = endpoint,
            payload = request.json()   
        )
    except Exception as error:
        logging.error(f"[-] Error : {error}")
        raise HTTPException(
            status_code = 500,
            detail = str(error)
        )
        
    return { "status" : "success" }
