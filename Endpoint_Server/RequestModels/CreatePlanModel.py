from pydantic import BaseModel
from Authentication.Authentication import Authentication
import pydantic

class CreatePlanRequest(BaseModel):
    sheet_id: str
    config_sheet_name: str
    data_sheet_name: str
    total_reach: int
    total_budget: float

    @pydantic.validator("sheet_id")
    @classmethod
    async def sheet_id_validator(cls, sheet_id) -> str:
        return sheet_id

    @pydantic.validator("config_sheet_name")
    @classmethod
    async def conifg_sheet_name_validator(cls, config_sheet_name) -> str:
        return config_sheet_name

    @pydantic.validator("data_sheet_name")
    @classmethod
    async def data_sheet_name_validator(cls, data_sheet_name) -> str:
        return data_sheet_name