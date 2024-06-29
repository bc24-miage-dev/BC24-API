from typing import Optional
from fastapi import APIRouter
from service.blockchain_service import BlockchainService
from service.private_key_service import PrivateKeyService


blockchainSerivce = BlockchainService()

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


@router.get("/TransferSingle")
async def get_single_transfer_events(
    receiver_address: Optional[str] = None,
    sender_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):
    logs = blockchainSerivce.get_events("TransferSingle")

    if receiver_address:
        logs = [log for log in logs if log["to"].lower() == receiver_address.lower()]
    if sender_address:
        logs = [log for log in logs if log["from"].lower() == sender_address.lower()]
    if tokenId:
        logs = [log for log in logs if log["id"] == tokenId]

    return {"event": "TransferSingle", "data": logs}


@router.get("/Creation")
async def get_creation_events(
    receiver_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):
    logs = blockchainSerivce.get_events("TransferSingle")
    logs = [
        log
        for log in logs
        if log["from"].lower() == "0x0000000000000000000000000000000000000000"
    ]

    if receiver_address:
        logs = [log for log in logs if log["to"].lower() == receiver_address.lower()]
    if tokenId:
        logs = [log for log in logs if log["id"] == tokenId]

    return {"event": "CreationEvents", "data": logs}


@router.get("/Burn")
async def get_burnt_events(
    sender_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):
    logs = blockchainSerivce.get_events("TransferSingle")
    logs = [
        log
        for log in logs
        if log["to"].lower() == "0x0000000000000000000000000000000000000000"
    ]

    if sender_address:
        logs = [log for log in logs if log["from"].lower() == sender_address.lower()]
    if tokenId:
        logs = [log for log in logs if log["id"] == tokenId]

    return {"event": "BurnEvent", "data": logs}


@router.get("/ResourceMetadataChanged")
async def get_metadata_changed_events(
    caller_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):
    logs = blockchainSerivce.get_events("ResourceMetaDataChangedEvent")

    if caller_address:
        logs = [log for log in logs if log["caller"].lower() == caller_address.lower()]
    if tokenId:
        logs = [log for log in logs if log["tokenId"] == tokenId]

    return {"event": "ResourceMetadataChanged", "data": logs}


@router.get("/ResourceCreated")
async def get_created_events(
    caller_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):
    logs = blockchainSerivce.get_events("ResourceCreatedEvent")

    if caller_address:
        logs = [log for log in logs if log["caller"].lower() == caller_address.lower()]
    if tokenId:
        logs = [log for log in logs if log["tokenId"] == tokenId]

    return {"event": "ResourceCreatedEvent", "data": logs}
