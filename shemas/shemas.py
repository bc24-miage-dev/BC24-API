
import json
from typing import Any, List
from pydantic import BaseModel


class RoleAssignmentRequest(BaseModel):
    from_wallet_address: str
    target_wallet_address: str
    role: str


class MintRessourceRequest(BaseModel):
    from_wallet_address: str
    resourceId: int
    quantity: int
    metaData: dict
    ingredients: list[int]


class MetaDataRequest(BaseModel):
    from_wallet_address: str
    tokenId: int
    metaData: dict


class MintToManyDataRequest(BaseModel):
    tokenId: int
    metaData: dict


class TransferResourceRequest(BaseModel):
    tokenId: int
    quantity: int
    from_wallet_address: str
    to_wallet_address: str


class ResourceTemplateResponse(BaseModel):
    resource_id: int
    resource_name: str
    needed_resources: List[Any]
    needed_resources_amounts: List[Any]
    initial_amount_minted: int
    required_role: str
    produces_resources: List[Any]
    produces_resources_amounts: List[Any]


class MetaDataResponse(BaseModel):
    data: List[Any]
    resource_id: int
    resource_name: str
    ingredients: List[Any]
