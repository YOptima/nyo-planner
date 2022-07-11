import logging

# Class to add context information to any request
# -- Context information is added through logging.Filters
# -- logging.Filter allows to manipulate log_record object to which we add the report_id
class ContextFilter(logging.Filter):
    '''Class to add report_id context to logs'''

    report_id: str

    # Initialise report_id to the filter 
    # -- report_id will be added to logger
    def __init__(self, report_id: str):
        self.report_id = report_id

    # Extending filter class to add report_id
    def filter(self, record):
        record.report_id = self.report_id
        return True