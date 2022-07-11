import json

from config import CONFIGURATION
from Authentication.Authentication import Authentication
from google.auth.credentials import Credentials
from TaskHandler.Exceptions import CreateTaskError

from google.cloud import tasks_v2
from pydantic import UUID4

# Logging COnfigurations
import logging
logger = logging.getLogger(__name__)

class TaskHandler():
    '''Wrapper class to google-cloud-tasksv2 to regulate queing operations'''

    credentials: Credentials
    client: tasks_v2.CloudTasksClient
    project_id: str
    location: str
    queue: str

    def __init__(self):

        auth_handler = Authentication()
        self.scopes = CONFIGURATION.get("SCOPES").get("CLOUD_TASK")
        self.credentials = auth_handler.getServiceAccountCredentials(scopes=self.scopes)
        
        self.client = tasks_v2.CloudTasksClient(credentials=self.credentials)

        self.queue = CONFIGURATION.get("QUEUE")
        self.project_id = CONFIGURATION.get("PROJECT_ID")
        self.location = CONFIGURATION.get("LOCATION")

    # Create HTTP-POST Task
    # -- Authorization - Bearer token
    def _getPOSTTask(self, endpoint: str, payload: dict, name: str = None) -> dict:

        logger.debug(f"[+] Creating Task ...")

        # Fetching Bearer token for the service account
        logger.debug(f"[+] Fetching Authentication Token")
        auth_handler = Authentication()

        # Create scaffold task
        # -- Bearer token authentication
        logger.debug(f"[+] Adding General Request Parameters")
        task = {
            "http_request": { 
                "http_method": "POST",
                "url": endpoint, 
                "headers" : { 
                    "Content-Type" : "application/json",
                },
                # "oidc_token" : {
                #     "service_account_email" : self.credentials.service_account_email,
                #     "audience" : endpoint
                # }
            }
        }

        # Add payload
        if payload:
            logger.debug(f"[+] Adding payload")
            payload_string = json.dumps(payload)
            payload_encoded = payload_string.encode()
            task["http_request"]["body"] = payload_encoded

        # Add Task Name
        if name: 
            logger.debug(f"[+] Adding Task Name")
            task["name"] = name

        logger.debug(f"[+] Task Created : {task}")
        return task

    def enqueueRequest(self, endpoint: str, payload: dict = None, task_id: str = None):
        
        # Get task 
        task_name = f"{self.queue}/tasks/{task_id}"
        task = self._getPOSTTask(endpoint, payload, task_name)

        try:
            # Enqueue task in queue
            logger.debug(f"[+] Enqueing Task ...")
            response = self.client.create_task({
                "parent" : self.queue,
                "task" : task
            })
            logger.debug(f"[+] Task added to the queue")
        except Exception as error:
            logger.error(f"[-] planner-task could not be added because {error}")
            raise CreateTaskError(
                task_id = task_name, 
                message = error
            )

        return { "success" : response }


        
