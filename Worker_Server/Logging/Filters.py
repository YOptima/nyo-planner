import logging
from config import REPORT_ID_CONTEXT

class ContextFilter(logging.Filter):

    def __init__(self) -> None:
        super()

    def filter(self, record) -> bool:
        report_id = REPORT_ID_CONTEXT.get()
        record.report_id = report_id
        return True