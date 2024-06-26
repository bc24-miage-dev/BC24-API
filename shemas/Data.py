from pydantic import BaseModel
from typing import Any

class Data(BaseModel):
    required_role: str
    stringData: Any
    lastModifiedBy: Any
    lastModifiedAt: int
