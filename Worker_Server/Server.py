import uvicorn
from Routes import app

# Logging Configurations
import logging
import logging.config
from config import LOGGING_CONFIGURATION
logging.config.dictConfig( LOGGING_CONFIGURATION )
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run( app = app )
