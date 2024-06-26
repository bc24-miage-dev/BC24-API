from pydantic import BaseModel
from typing import Any, List

class ResourceTemplateResponse(BaseModel):
    resource_id: int
    resource_name: str
    needed_resources: List[Any]
    needed_resources_amounts: List[Any]
    initial_amount_minted: int
    required_role: str
    produces_resources: List[Any]
    produces_resources_amounts: List[Any]
    resource_type: str
