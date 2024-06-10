
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

class TransferResource(BaseModel):
    tokenId: int
    quantity: int
    wallet_address_owner: str
    wallet_address_receiver: str