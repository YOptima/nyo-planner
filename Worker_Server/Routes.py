from config import REPORT_ID_CONTEXT

# Logging Configurations
import logging
logger = logging.getLogger(__name__)


# Fast API Configurations
from fastapi import FastAPI, HTTPException, Request
app = FastAPI()


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