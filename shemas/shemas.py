import json
from typing import Any, List, Optional
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


class MintOneToManyRessourceRequest(BaseModel):
    from_wallet_address: str
    producer_token_id: int
    metaData: dict


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
    resource_type: str


class Data(BaseModel):
    required_role: str
    stringData: Any
    lastModifiedBy: Any
    lastModifiedAt: int


class MetaData(BaseModel):
    data: List[Data]
    resource_id: int
    resource_name: str
    resource_type: str
    ingredients: List[Any]

class MetaDataResponse(BaseModel):
    tokenId: int
    balance: int
    metaData: Optional[MetaData] = None


class ResourceCreatedEventResponse(BaseModel):
    tokenId:str
    ressourceName:str
    message:str
    caller:str


class CreateWalletResponse(BaseModel):
    wallet_address: str

class RoleResponse(BaseModel):
    role: str


class EventResponse(BaseModel):
    event: str
    data: List[dict]

class ResourceMetaDataChangedEventResponse(BaseModel):
    tokenId: int
    metaData: dict
    caller: str