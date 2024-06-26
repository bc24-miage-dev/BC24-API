from pydantic import BaseModel

class ResourceCreatedEventResponse(BaseModel):
    tokenId: int
    ressourceName: str
    message: str
    caller: str
