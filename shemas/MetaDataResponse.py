from pydantic import BaseModel
from typing import Optional
from shemas.MetaData import MetaData

class MetaDataResponse(BaseModel):
    tokenId: int
    balance: int
    metaData: Optional[MetaData] = None
