from pydantic import BaseModel
from typing import Any, List, Optional

class MintRessourceRequest(BaseModel):
    from_wallet_address: str
    resourceId: int
    quantity: int
    metaData: dict
    ingredients: list[int]
