from pydantic import BaseModel

class TransferResourceResponse(BaseModel):
    tokenId: int
    quantity: int
    from_wallet_address: str
    to_wallet_address: str
