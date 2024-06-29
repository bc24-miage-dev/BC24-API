import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from service.blockchain_service import BlockchainService
from service.event_service import EventService
from service.private_key_service import PrivateKeyService
from service.resource_service import ResourceService
from shemas.Data import Data
from shemas.MetaData import MetaData
from shemas.MetaDataRequest import MetaDataRequest
from shemas.MetaDataResponse import MetaDataResponse
from shemas.MintOneToManyRessourceRequest import MintOneToManyRessourceRequest
from shemas.MintRessourceRequest import MintRessourceRequest
from shemas.ResourceCreatedEventResponse import ResourceCreatedEventResponse
from shemas.ResourceMetaDataChangedEventResponse import (
    ResourceMetaDataChangedEventResponse,
)
from shemas.ResourceTemplateResponse import ResourceTemplateResponse
from shemas.TransferResourceRequest import TransferResourceRequest
from shemas.TransferResourceResponse import TransferResourceResponse

resource_service = ResourceService()
event_service = EventService()
private_key_service = PrivateKeyService()

router = APIRouter(
    prefix="/resource",
)


@router.get(
    "/templates",
    response_model=List[ResourceTemplateResponse],
    tags=["resource"],
)
async def get_resources_templates(
    resource_id: Optional[int] = None, required_role: Optional[str] = None
):
    try:
        resources_templates = resource_service.get_templates()

        filtered_resources = [
            ResourceTemplateResponse(
                resource_id=template[0],
                resource_name=template[1],
                needed_resources=template[2],
                needed_resources_amounts=template[3],
                initial_amount_minted=template[4],
                required_role=template[5],
                produces_resources=template[6],
                produces_resources_amounts=template[7],
                resource_type=template[8],
            )
            for template in resources_templates
            if (resource_id is None or template[0] == resource_id)
            and (required_role is None or template[5] == required_role)
        ]

        return filtered_resources

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get resources_templates: {e}"
        )


@router.post(
    "/mint",
    response_model=ResourceCreatedEventResponse | List[ResourceCreatedEventResponse],
    tags=["resource"],
)
async def create_resource(request: MintRessourceRequest):
    try:

        from_wallet_private_key = private_key_service.get_private_key(
            request.from_wallet_address
        )

        resource_id = request.resourceId
        quantity = request.quantity
        meta_data = json.dumps(request.metaData, indent=4)
        ingredients = request.ingredients

        txn_receipt = resource_service.mint_resource(
            from_wallet_private_key, resource_id, quantity, meta_data, ingredients
        )

        resource_created_events = event_service.get_resource_created_event_by_receipt(
            txn_receipt
        )

        return_object = [
            ResourceCreatedEventResponse(
                tokenId=event.args.tokenId,
                ressourceName=event.args.ressourceName,
                message=event.args.message,
                caller=event.args.caller,
            )
            for event in resource_created_events
        ]

        return return_object[0]

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.post(
    "/mintToMany",
    response_model=List[ResourceCreatedEventResponse],
    tags=["resource"],
)
async def create_resource_one_to_many(request: MintOneToManyRessourceRequest):
    try:

        from_wallet_private_key = private_key_service.get_private_key(
            request.from_wallet_address
        )

        producer_token_id = request.producer_token_id
        meta_data = json.dumps(request.metaData, indent=4)

        txn_receipt = resource_service.mint_one_to_many_resource(
            from_wallet_private_key, producer_token_id, meta_data
        )

        resource_created_events = event_service.get_resource_created_event_by_receipt(
            txn_receipt
        )

        return_events = [
            ResourceCreatedEventResponse(
                tokenId=event.args.tokenId,
                ressourceName=event.args.ressourceName,
                message=event.args.message,
                caller=event.args.caller,
            )
            for event in resource_created_events
        ]

        return return_events

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.post(
    "/transfer",
    response_model=TransferResourceResponse,
    tags=["resource"],
)
async def transfer_resource(request: TransferResourceRequest):
    try:

        from_wallet_private_key = private_key_service.get_private_key(
            request.from_wallet_address
        )

        from_wallet_address = request.from_wallet_address
        to_wallet_address = request.to_wallet_address
        tokenId = request.tokenId
        quantity = request.quantity

        txn_receipt = resource_service.transfer_resource(
            from_wallet_private_key,
            from_wallet_address,
            to_wallet_address,
            tokenId,
            quantity,
        )

        resource_transferred_events = (
            event_service.get_resource_transferred_event_by_receipt(txn_receipt)
        )

        event = resource_transferred_events[0]

        return_object = TransferResourceResponse(
            tokenId=event.args.id,
            quantity=event.args.value,
            from_wallet_address=event.args["from"],
            to_wallet_address=event.args.to,
        )

        return return_object
    except Exception as e:
        print(e)
        if str(e) == "Invalid wallet address":
            raise HTTPException(status_code=400, detail=str(e))
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.post(
    "/metadata",
    response_model=ResourceMetaDataChangedEventResponse,
    summary="Create Resource Metadata",
    description="Creates a new resource metadata entry.",
    responses={
        429: {"description": "Too Many Requests - Rate limit exceeded."},
    },
    tags=["metadata"],
)
async def set_metadata(request: MetaDataRequest):
    try:

        token_id = request.tokenId
        meta_data = json.dumps(request.metaData, indent=4)
        from_wallet_address = request.from_wallet_address

        from_wallet_private_key = private_key_service.get_private_key(
            from_wallet_address
        )

        txn_receipt = resource_service.set_metadata(
            from_wallet_private_key, from_wallet_address, token_id, meta_data
        )

        resource_metaDataEvent = (
            event_service.get_resource_metaData_changed_event_by_receipt(txn_receipt)
        )

        if len(resource_metaDataEvent) == 0:
            raise HTTPException(
                status_code=429,
                detail=f"Too Many Requests - Rate limit exceeded.",
            )

        metadata = resource_metaDataEvent[0].args.metaData
        resource_metaData = metadata.data
        resource_id = metadata.resourceId
        resource_name = metadata.ressourceName
        resource_type = metadata.ressourceType
        ingredients_token_ids = metadata.ingredients

        transformed_metaData = [
            Data(
                required_role=data.required_role,
                stringData=json.loads(data.dataString),
                lastModifiedBy=data.lastModifiedBy,
                lastModifiedAt=data.lastModifiedAt,
            )
            for data in resource_metaData
        ]

        return_metaData = MetaData(
            owner=request.from_wallet_address,
            data=transformed_metaData,
            resource_id=resource_id,
            resource_name=resource_name,
            resource_type=resource_type,
            ingredients=ingredients_token_ids,
        )

        return_object = ResourceMetaDataChangedEventResponse(
            tokenId=resource_metaDataEvent[0].args.tokenId,
            metaData=return_metaData,
            caller=resource_metaDataEvent[0].args.caller,
        )

        return return_object
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.get(
    "/{wallet_address}",
    response_model=List[MetaDataResponse],
    tags=["metadata"],
)
async def get_resource_by_wallet_address_with_optional_metaData(
    wallet_address: str,
    metaData: Optional[bool] = False,
    recursive: Optional[bool] = False,
):
    try:
        verify_wallet_address = private_key_service.get_private_key(wallet_address)
        events = event_service.get_events("TransferSingle")

        # filter only wallet address relevant events
        to_events = [event for event in events if event["to"] == wallet_address]
        from_events = [event for event in events if event["from"] == wallet_address]

        active_tokens = {}

        for event in to_events:
            token_id = event.id
            value = event.value

            if token_id in active_tokens:
                active_tokens[token_id] += value
            else:
                active_tokens[token_id] = value

        for event in from_events:
            token_id = event.id
            value = event.value

            active_tokens[token_id] = -value

        # Filter out tokens with zero balance
        active_tokens = {
            token_id: balance
            for token_id, balance in active_tokens.items()
            if balance > 0
        }

        enriched_metadata_of_tokens = resource_service.get_enriched_metadata_of_tokens(
            active_tokens, metaData, recursive
        )

        return enriched_metadata_of_tokens

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=e)


@router.get("/{tokenId}/metadata", response_model=MetaData, tags=["metadata"])
async def get_metadata_of_resource(tokenId: int, recursive: Optional[bool] = False):
    try:

        enriched_metadata = resource_service.fetch_and_enrich_metadata(
            tokenId, recursive
        )

        transfer_events = event_service.get_events("TransferSingle")
        token_logs = [log for log in transfer_events if log["id"] == tokenId]
        token_owner = token_logs[-1]["to"]

        enriched_metadata.current_owner = token_owner

        enriched_metadata.quantity = resource_service.get_balance_of_token(
            token_owner, tokenId
        )

        return enriched_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metadata: {e}")
