from pydantic import BaseModel

class TransactionRequest(BaseModel):
    sender_address: str
    receiver_address: str
    amount: float  # Amount in Ether
