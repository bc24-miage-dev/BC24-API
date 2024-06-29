from pydantic import BaseModel
from shemas.MetaData import MetaData

class ResourceMetaDataChangedEventResponse(BaseModel):
    tokenId: int
    metaData: MetaData 
    caller: str
