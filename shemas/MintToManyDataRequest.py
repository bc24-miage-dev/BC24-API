from pydantic import BaseModel

class MintToManyDataRequest(BaseModel):
    tokenId: int
    metaData: dict
