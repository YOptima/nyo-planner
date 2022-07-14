# Fast API Configurations
from fastapi import FastAPI, HTTPException, Request
from h11 import Data
app = FastAPI()


# Logging Configurations
import logging
logger = logging.getLogger(__name__)


from config import REPORT_ID_CONTEXT
from RequestModels.WorkerCreatePlanModel import WorkerCreatePlanRequest
from GoogleSheets.GoogleSheets import GoogleSheets 
from pandas import DataFrame

# Context Middleware
@app.middleware("http")
async def context_middelware(request: Request, call_next):

    headers = request.headers
    report_id = headers.get("X-Request-ID")
    REPORT_ID_CONTEXT.set(report_id)

    try:
        response = await call_next( request )
    except Exception as error:
        logger.error(f"[-] Request Failed")
        raise HTTPException(
            status = 500,
            detail = "Unable to Serve Request" 
        )
    finally: 
        assert report_id == REPORT_ID_CONTEXT.get()
        logger.debug("[+] Request Ended")
        return response

@app.post("/worker/create")
async def createPlan(request: WorkerCreatePlanRequest):

    sheet_id: str = request.sheet_id
    gsheet_handler: GoogleSheets = GoogleSheets()
    
    # Fetching Global Config Sheet Data
    global_config_sheet_name: str = request.global_config_sheet_name
    global_config_sheet_dataframe: DataFrame = gsheet_handler.fetchData(
        spreadsheet_id = sheet_id,
        sheet_name = global_config_sheet_name
    )
    print( global_config_sheet_dataframe )

    # Fetching Config Sheet Data
    config_sheet_name: str = request.config_sheet_name
    config_sheet_dataframe: DataFrame = gsheet_handler.fetchData(
        spreadsheet_id = sheet_id,
        sheet_name = config_sheet_name
    )
    print( config_sheet_dataframe )

    # Fetching Budget Based Data
    data_sheet_name: str = request.data_sheet_name
    data_sheet_dataframe: DataFrame = gsheet_handler.fetchData(
        spreadsheet_id = sheet_id,
        sheet_name = data_sheet_name  
    )
    print( data_sheet_dataframe )