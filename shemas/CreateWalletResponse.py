from pydantic import BaseModel

class CreateWalletResponse(BaseModel):
    wallet_address: str
