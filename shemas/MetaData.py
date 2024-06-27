from pydantic import BaseModel
from typing import Any, List, Optional
from shemas.Data import Data

class MetaData(BaseModel):
    data: List[Data]
    resource_id: int
    resource_name: str
    resource_type: str
    ingredients: List[Any]
    current_owner: Optional[str] = None
