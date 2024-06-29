from pydantic import BaseModel

class TransferResourceRequest(BaseModel):
    tokenId: int
    quantity: int
    from_wallet_address: str
    to_wallet_address: str
