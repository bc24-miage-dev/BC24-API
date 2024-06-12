import json
from fastapi import APIRouter, HTTPException, status
from service.walletService import PrivateKeyService
from shemas.shemas import *
from core.config import contract_settings
from web3.middleware import geth_poa_middleware
from web3 import Web3
from typing import List, Optional

web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = web3.eth.contract(
    address=contract_settings.contract_address, abi=contract_settings.contract_abi)

private_key_service = PrivateKeyService()


router = APIRouter()


@router.get("/roles")
async def get_roles():
    try:
        resources = contract.functions.getResourceTemplates().call()
        roles = list(set([resource[5] for resource in resources]))
        return roles
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get roles: {e}")


@router.get("/roles/{wallet_address}")
async def get_role_of_wallet_address(wallet_address: str):
    try:
        roles = contract.functions.userRoles(wallet_address).call()
        return {"role": roles}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get roles: {e}")


@router.post("/roles/assignRole")
async def assign_role(request: RoleAssignmentRequest):
    if not web3.is_address(request.from_wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    if not web3.is_address(request.target_wallet_address):
        raise HTTPException(
            status_code=400, detail="Invalid target wallet address")
    try:
        # TODO: Replace these with your account details
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address))

        txn_dict = contract.functions.giveUserRole(request.target_wallet_address, request.role).build_transaction({
            "from": account.address,
            'chainId': 1337,
            'nonce': web3.eth.get_transaction_count(account.address),
        })

        signed_txn = web3.eth.account.sign_transaction(
            txn_dict, private_key=account.key)

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        web3.eth.wait_for_transaction_receipt(txn_hash)

        return {"status": "Role assigned successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/resourceTemplates", response_model=List[ResourceTemplateResponse])
async def get_resources_templates(resource_id: Optional[int] = None, required_role: Optional[str] = None):
    try:
        resources = contract.functions.getResourceTemplates().call()

        filtered_resources = [
            ResourceTemplateResponse(
                resource_id=resource[0],
                resource_name=resource[1],
                needed_resources=resource[2],
                needed_resources_amounts=resource[3],
                initial_amount_minted=resource[4],
                required_role=resource[5],
                produces_resources=resource[6],
                produces_resources_amounts=resource[7],
            )
            for resource in resources
            if (resource_id is None or resource[0] == resource_id) and (required_role is None or resource[5] == required_role)
        ]

        return filtered_resources

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get resources: {e}")


@router.post("/mintResource")
async def mint_resource(request: MintRessourceRequest):
    try:
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address))

        resource_id = request.resourceId
        quantity = request.quantity
        meta_data = json.dumps(request.metaData, indent=4)

        ingredients = request.ingredients

        transaction = contract.functions.mintRessource(resource_id, quantity, meta_data, ingredients).build_transaction({
            "from": account.address,
            'chainId': 1337,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        })

        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key)

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_created_events = contract.events.ResourceCreatedEvent(
        ).process_receipt(txn_receipt)

        return resource_created_events[0].args

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")


@router.post("/mintOneToMany")
async def mint_one_to_many(data: MintToManyDataRequest):
    return "to implement"


@router.get("/metadata/{tokenId}")
async def metadata(tokenId: int):
    try:
        enriched_metadata = fetch_and_enrich_metadata(tokenId)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get metadata: {e}")

    return enriched_metadata


def fetch_and_enrich_metadata(tokenId):
    metadata = contract.functions.getMetaData(tokenId).call()

    enriched_ingredients = []
    ingredients_token_ids = metadata[3]

    if ingredients_token_ids:
        for ingredient_tokenId in metadata[3]:
            enriched_ingredient = fetch_and_enrich_metadata(ingredient_tokenId)
            enriched_ingredients.append(enriched_ingredient)

    return MetaDataResponse(data=metadata[0],
                            resource_id=metadata[1],
                            resource_name=metadata[2],
                            ingredients=enriched_ingredients)


@router.post("/metadata")
async def set_metadata(request: MetaDataRequest):
    if not web3.is_address(request.from_wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    try:
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address))

        token_id = request.tokenId
        meta_data = json.dumps(request.metaData, indent=4)

        transaction = contract.functions.setMetaData(token_id, meta_data).build_transaction({
            "from": account.address,
            'chainId': 1337,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        })

        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key)

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_metaDataEvent = contract.events.ResourceMetaDataChangedEvent(
        ).process_receipt(txn_receipt)

        return resource_metaDataEvent[0].args
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/tokens/{wallet_address}")
async def get_resources_by_wallet_address(wallet_address: str):
    if not web3.is_address(wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    try:
        start_block = 0
        end_block = web3.eth.block_number
        active_tokens = {}

        # Fetch TransferSingle events in batches
        for block in range(start_block, end_block + 1, 1000):  # Adjust batch size as needed
            batch_end_block = min(block + 999, end_block)
            events = contract.events.TransferSingle.get_logs(
                fromBlock=block, toBlock=batch_end_block)

            for event in events:
                event_args = event['args']
                from_address = event_args['from']
                to_address = event_args['to']
                token_id = event_args['id']
                value = event_args['value']

                # If the token was transferred to the wallet_address, mark it as active
                if to_address.lower() == wallet_address.lower():
                    if token_id not in active_tokens:
                        active_tokens[token_id] = value
                    else:
                        active_tokens[token_id] += value

                # If the token was transferred from the wallet_address, reduce its count or remove it
                if from_address.lower() == wallet_address.lower():
                    if token_id in active_tokens:
                        if active_tokens[token_id] <= value:
                            del active_tokens[token_id]
                        else:
                            active_tokens[token_id] -= value

        # Filter out tokens with zero balance
        active_tokens = {token_id: balance for token_id,
                         balance in active_tokens.items() if balance > 0}

        return {"active_tokens for account": active_tokens}
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")


@router.post("/transfer")
async def transfer_resource(transfer: TransferResourceRequest):
    # Check if the sender s wallet addresses is valid
    if (not web3.is_address(transfer.wallet_address_owner)):
        raise HTTPException(
            status_code=400, detail="Invalid wallet address for the sender")
    if (not web3.is_address(transfer.wallet_address_receiver)):
        raise HTTPException(
            status_code=400, detail="Invalid wallet address for the receiver")
    try:

        account = web3.eth.account.from_key(
            private_key_service.get_private_key(transfer.from_wallet_address))

        txn_dict = contract.functions.safeTransferFrom(transfer.from_wallet_address,
                                                       transfer.to_wallet_address,
                                                       transfer.tokenId,
                                                       transfer.quantity,
                                                       b'').build_transaction({
                                                           "from": account.address,
                                                           'chainId': 1337,
                                                           'nonce': web3.eth.get_transaction_count(account.address),
                                                       })

        signed_txn = web3.eth.account.sign_transaction(
            txn_dict, private_key=account.key)

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
        return {"status": "success", }
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/events/{event}")
async def get_event_logs(event: str):

    start_block = 0
    end_block = web3.eth.block_number
    batch_size = 1000

    logs = []
    for block in range(start_block, end_block + 1, batch_size):
        batch_end_block = min(block + batch_size - 1, end_block)
        events = contract.events[event].get_logs(
            fromBlock=block, toBlock=batch_end_block)
        logs += [event.args for event in events]

    return {"event": event, "data": logs}
