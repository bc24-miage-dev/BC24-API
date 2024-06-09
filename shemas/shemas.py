from pydantic import BaseModel


class RoleAssignment(BaseModel):
    wallet_address: str
    role: str
