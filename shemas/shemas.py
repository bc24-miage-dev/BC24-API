
import json
from typing import Any, List
from pydantic import BaseModel


class RoleAssignment(BaseModel):
    wallet_address: str
    role: str


class MintRessource(BaseModel):
    resourceId: int
    quantity: int
    metaData: dict
    ingredients: list[int]


class MetaData(BaseModel):
    tokenId: int
    metaData: dict


class MintToManyData(BaseModel):
    tokenId: int
    metaData: dict

class ResourceTemplateResponse(BaseModel):
    resource_id: int
    resource_name: str
    needed_resources: List[Any]
    needed_resources_amounts: List[Any]
    initial_amount_minted: int
    required_role: str
    produces_resources: List[Any]
    produces_resources_amounts: List[Any]
