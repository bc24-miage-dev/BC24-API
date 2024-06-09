
import json
from pydantic import BaseModel


class RoleAssignment(BaseModel):
    wallet_address: str
    role: str


class MintRessource(BaseModel):
    resourceId: int
    quantity: int
    _metaData: str
    ingredients: list


class MetaData(BaseModel):
    tokenId: int
    metaData: dict


class MintToManyData(BaseModel):
    tokenId: int
    metaData: dict
