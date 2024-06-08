from pydantic import BaseModel


class Example(BaseModel):
    name: str
    song: str


class RoleAssignment(BaseModel):
    wallet_address: str
    role: str
