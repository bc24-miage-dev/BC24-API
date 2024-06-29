from pydantic import BaseModel

class RoleResponse(BaseModel):
    role: str
