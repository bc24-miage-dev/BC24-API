import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException

from service.event_service import EventService
from service.private_key_service import PrivateKeyService
from service.resource_service import ResourceService
from shemas.MintRessourceRequest import MintRessourceRequest
from shemas.ResourceCreatedEventResponse import ResourceCreatedEventResponse
from shemas.ResourceTemplateResponse import ResourceTemplateResponse


resource_service = ResourceService()
event_service = EventService()
private_key_service = PrivateKeyService()

router = APIRouter(
    prefix="/resource",
    tags=["resource"],
)


@router.get("/templates", response_model=List[ResourceTemplateResponse])
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
    "/resource/mint",
    response_model=ResourceCreatedEventResponse | List[ResourceCreatedEventResponse],
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
