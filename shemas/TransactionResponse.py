from pydantic import BaseModel

class TransactionResponse(BaseModel):
    transaction_hash: str
    details: str
