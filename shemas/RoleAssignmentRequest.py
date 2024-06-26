from pydantic import BaseModel

class RoleAssignmentRequest(BaseModel):
    from_wallet_address: str
    target_wallet_address: str
    role: str
