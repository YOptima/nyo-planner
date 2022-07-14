from pydantic import BaseModel
import pydantic

class WorkerCreatePlanRequest(BaseModel):
    sheet_id: str
    global_config_sheet_name: str
    config_sheet_name: str
    data_sheet_name: str
    total_reach: int
    total_budget: float

    @pydantic.validator("sheet_id")
    def sheet_id_validator(cls, sheet_id) -> str:
        return sheet_id

    @pydantic.validator("global_config_sheet_name")
    def global_config_sheet_name_validator(cls, global_config_sheet_name) -> str:
        return global_config_sheet_name

    @pydantic.validator("config_sheet_name")
    def conifg_sheet_name_validator(cls, config_sheet_name) -> str:
        return config_sheet_name

    @pydantic.validator("data_sheet_name")
    def data_sheet_name_validator(cls, data_sheet_name) -> str:
        return data_sheet_name

    @pydantic.validator("total_reach")
    def total_reach_validator(cls, total_reach) -> int:
        return total_reach

    @pydantic.validator("total_budget")
    def total_udget_validator(cls, total_budget) -> float:
        return total_budget