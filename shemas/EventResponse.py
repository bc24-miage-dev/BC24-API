from pydantic import BaseModel
from typing import List

class EventResponse(BaseModel):
    event: str
    data: List[dict]
