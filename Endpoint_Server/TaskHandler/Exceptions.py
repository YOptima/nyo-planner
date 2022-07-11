class CreateTaskError(Exception):
    '''Exception class for handling create task error'''

    def __init__(self, task_id: str, message: str) -> None:
        self.task_id = task_id
        self.error_message = message
        self.message = f"{self.task_id} : Failure : {self.error_message}" 
        super().__init__(self.message)