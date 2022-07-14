import gspread
from gspread.client import Client
from gspread.spreadsheet import Spreadsheet
from gspread.worksheet import Worksheet
from pandas import DataFrame
from typing import List

from config import CONFIGURATION
from Authentication.Authentication import Authentication
from google.auth.credentials import Credentials

# Logging Configurations
import logging
logger = logging.getLogger(__name__)

class GoogleSheets:

    credentials: Credentials
    client: Client

    def __init__(self) -> None:
        
        auth_handler: Authentication = Authentication()
        self.credentials = auth_handler.getServiceAccountCredentials()

        self.client = gspread.authorize(self.credentials)


    def fetchData( self, spreadsheet_id: str, sheet_name: str ) -> DataFrame: 
        '''Fetch GoogleSheets Data
        Arguments: 
            - spreadsheet_id (str) : id of the spreadsheet to fetch data from
            - sheet_name (str) : name of the sheet within the spreadsheet where the data resides
        Returns:
            - pandas.DataFrame
        '''
        
        logger.debug(f"[+] Initialising Worksheet to extract data")
        logger.debug(f"[+] Spreadsheet_ID: {spreadsheet_id}")
        logger.debug(f"[+] Spreadsheet_Name: {sheet_name}")
        spreadsheet: Spreadsheet = self.client.open_by_key(spreadsheet_id)
        worksheet: Worksheet = spreadsheet.worksheet(sheet_name)

        records: List[dict] = worksheet.get_all_records()

        return DataFrame( records )
