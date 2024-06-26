from pydantic import BaseModel

class MetaDataRequest(BaseModel):
    from_wallet_address: str
    tokenId: int
    metaData: dict
