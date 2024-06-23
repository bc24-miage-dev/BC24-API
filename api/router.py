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
    address=contract_settings.contract_address, abi=contract_settings.contract_abi
)

private_key_service = PrivateKeyService()


router = APIRouter()


@router.get("/wallet/create", response_model=CreateWalletResponse)
async def create_wallet():
    acc = web3.eth.account.create()
    private_key_service.add_private_key(acc.address, web3.to_hex(acc.key))

    return {"wallet_address": acc.address}


@router.get("/wallet/static", response_model=CreateWalletResponse)
async def create_wallet():

    return {"wallet_address": "0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6"}


@router.post("/wallet/send-eth", response_model=TransactionResponse)
async def send_eth(transaction_request: TransactionRequest):
    sender_address = transaction_request.sender_address
    receiver_address = transaction_request.receiver_address
    amount_in_ether = transaction_request.amount
    amount_in_wei = web3.to_wei(amount_in_ether, 'ether')

    # Retrieve the private key securely
    try:
        private_key = private_key_service.get_private_key(sender_address)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sender address not found")

    # Build and sign the transaction
    nonce = web3.eth.get_transaction_count(sender_address)
    txn = {
        'nonce': nonce,
        'to': receiver_address,
        'value': amount_in_wei,
        'gas': 2000000,
        'gasPrice': web3.to_wei('50', 'gwei'),
    }
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_hash_hex = web3.to_hex(txn_hash)

    return {"transaction_hash": txn_hash_hex, "details": "ETH deposited successfully"}


@router.get("/roles", response_model=List[str])
async def get_available_roles():
    try:
        resources = contract.functions.getResourceTemplates().call()
        roles = list(set([resource[5] for resource in resources]))
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roles: {e}")


@router.get("/roles/{wallet_address}", response_model=RoleResponse)
async def get_role_of_wallet_address(wallet_address: str):
    try:
        roles = contract.functions.userRoles(wallet_address).call()
        return {"role": roles}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get roles: {e}")


@router.post("/roles/assignRole")
async def assign_role_to_user(request: RoleAssignmentRequest):
    if not web3.is_address(request.from_wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    if not web3.is_address(request.target_wallet_address):
        raise HTTPException(status_code=400, detail="Invalid target wallet address")
    try:
        # TODO: Replace these with your account details
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address)
        )

        txn_dict = contract.functions.giveUserRole(
            request.target_wallet_address, request.role
        ).build_transaction(
            {
                "from": account.address,
                "chainId": 1337,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = web3.eth.account.sign_transaction(
            txn_dict, private_key=account.key
        )

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        web3.eth.wait_for_transaction_receipt(txn_hash)

        return {"status": "Role assigned successfully"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/resource/templates", response_model=List[ResourceTemplateResponse])
async def get_resources_templates(
    resource_id: Optional[int] = None, required_role: Optional[str] = None
):
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
                resource_type=resource[8],
            )
            for resource in resources
            if (resource_id is None or resource[0] == resource_id)
            and (required_role is None or resource[5] == required_role)
        ]

        return filtered_resources

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get resources: {e}")


@router.post("/resource/mint", response_model=ResourceCreatedEventResponse)
async def create_resource(request: MintRessourceRequest):
    try:
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address)
        )

        resource_id = request.resourceId
        quantity = request.quantity
        meta_data = json.dumps(request.metaData, indent=4)

        ingredients = request.ingredients

        transaction = contract.functions.mintRessource(
            resource_id, quantity, meta_data, ingredients
        ).build_transaction(
            {
                "from": account.address,
                "chainId": 1337,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key
        )

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_created_events = (
            contract.events.ResourceCreatedEvent().process_receipt(txn_receipt)
        )

        return_object = ResourceCreatedEventResponse(
            tokenId=resource_created_events[0].args.tokenId,
            ressourceName=resource_created_events[0].args.ressourceName,
            message=resource_created_events[0].args.message,
            caller=resource_created_events[0].args.caller,
        )

        return return_object

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.post("/resource/mintToMany", response_model=List[ResourceCreatedEventResponse])
async def create_resource_one_to_many(request: MintOneToManyRessourceRequest):
    try:
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address)
        )

        producer_token_id = request.producer_token_id

        meta_data = json.dumps(request.metaData, indent=4)

        transaction = contract.functions.mintOneToMany(
            producer_token_id, meta_data
        ).build_transaction(
            {
                "from": account.address,
                "chainId": 1337,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key
        )

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_created_events = (
            contract.events.ResourceCreatedEvent().process_receipt(txn_receipt)
        )

        return_events = [
            ResourceCreatedEventResponse(
                tokenId=transaction_event.args.tokenId,
                ressourceName=transaction_event.args.ressourceName,
                message=transaction_event.args.message,
                caller=transaction_event.args.caller,
            )
            for transaction_event in resource_created_events
        ]

        return return_events

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/resource/{wallet_address}", response_model=List[MetaDataResponse])
async def get_resource_by_wallet_address_with_optional_metaData(
    wallet_address: str,
    metaData: Optional[bool] = False,
    recursive: Optional[bool] = False,
):
    if not web3.is_address(wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    try:
        start_block = 0
        end_block = web3.eth.block_number
        active_tokens = {}

        # Fetch TransferSingle events in batches
        for block in range(
            start_block, end_block + 1, 1000
        ):  # Adjust batch size as needed
            batch_end_block = min(block + 999, end_block)
            events = contract.events.TransferSingle.get_logs(
                fromBlock=block, toBlock=batch_end_block
            )

            for event in events:
                event_args = event["args"]
                from_address = event_args["from"]
                to_address = event_args["to"]
                token_id = event_args["id"]
                value = event_args["value"]

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
        active_tokens = {
            token_id: balance
            for token_id, balance in active_tokens.items()
            if balance > 0
        }

        active_resources = []

        for token_id in active_tokens:
            resource = {"tokenId": token_id, "balance": active_tokens[token_id]}
            if metaData:
                enriched_metadata = fetch_and_enrich_metadata(
                    contract, token_id, recursive
                )
                resource = {**resource, "metaData": enriched_metadata}

            active_resources.append(resource)

        return active_resources

    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.post("/resource/transfer")
async def transfer_resource(transfer: TransferResourceRequest):
    # Check if the sender s wallet addresses is valid
    if not web3.is_address(transfer.from_wallet_address):
        raise HTTPException(
            status_code=400, detail="Invalid wallet address for the sender"
        )
    if not web3.is_address(transfer.to_wallet_address):
        raise HTTPException(
            status_code=400, detail="Invalid wallet address for the receiver"
        )
    try:

        account = web3.eth.account.from_key(
            private_key_service.get_private_key(transfer.from_wallet_address)
        )

        txn_dict = contract.functions.safeTransferFrom(
            transfer.from_wallet_address,
            transfer.to_wallet_address,
            transfer.tokenId,
            transfer.quantity,
            b"",
        ).build_transaction(
            {
                "from": account.address,
                "chainId": 1337,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = web3.eth.account.sign_transaction(
            txn_dict, private_key=account.key
        )

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_transferred_events = contract.events.TransferSingle().process_receipt(
            txn_receipt
        )

        return resource_transferred_events[0].args
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/resource/{tokenId}/metadata", response_model=MetaData)
async def get_metadata_of_resource(tokenId: int, recursive: Optional[bool] = False):
    try:
        enriched_metadata = fetch_and_enrich_metadata(contract, tokenId, recursive)

        return enriched_metadata
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get metadata: {e}")


def fetch_and_enrich_metadata(contract, tokenId, recursive=True):
    metadata = contract.functions.getMetaData(tokenId).call()

    resource_metaData = metadata[0]
    resource_id = metadata[1]
    resource_name = metadata[2]
    resource_type = metadata[3]
    ingredients_token_ids = metadata[4]

    enriched_ingredients = []

    if recursive:
        for ingredient_tokenId in ingredients_token_ids:
            enriched_ingredient = fetch_and_enrich_metadata(
                contract, ingredient_tokenId
            )
            enriched_ingredients.append(enriched_ingredient)
    else:
        enriched_ingredients = ingredients_token_ids

    transformed_metaData = [
        Data(
            required_role=data[0],
            stringData=json.loads(data[1]),
            lastModifiedBy=data[2],
            lastModifiedAt=data[3],
        )
        for data in resource_metaData
    ]

    return MetaData(
        data=transformed_metaData,
        resource_id=resource_id,
        resource_name=resource_name,
        resource_type=resource_type,
        ingredients=enriched_ingredients,
    )


@router.post("/resource/metadata", response_model=ResourceMetaDataChangedEventResponse)
async def set_metadata(request: MetaDataRequest):
    if not web3.is_address(request.from_wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    try:
        account = web3.eth.account.from_key(
            private_key_service.get_private_key(request.from_wallet_address)
        )

        token_id = request.tokenId
        meta_data = json.dumps(request.metaData, indent=4)

        transaction = contract.functions.setMetaData(
            token_id, meta_data
        ).build_transaction(
            {
                "from": account.address,
                "chainId": 1337,
                "gasPrice": web3.eth.gas_price,
                "nonce": web3.eth.get_transaction_count(account.address),
            }
        )

        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key
        )

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        resource_metaDataEvent = (
            contract.events.ResourceMetaDataChangedEvent().process_receipt(txn_receipt)
        )

        return_object = ResourceMetaDataChangedEventResponse(
            tokenId=resource_metaDataEvent[0].args.tokenId,
            ressourceName=resource_metaDataEvent[0].args.ressourceName,
            message=resource_metaDataEvent[0].args.message,
            caller=resource_metaDataEvent[0].args.caller,
        )

        return return_object
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=f"Failed to send transaction: {e}")


@router.get("/events/{event}", response_model=EventResponse)
async def get_event_logs_with_optional_filters(
    event: str,
    receiver_address: Optional[str] = None,
    sender_address: Optional[str] = None,
    tokenId: Optional[int] = None,
):

    start_block = 0
    end_block = web3.eth.block_number
    batch_size = 1000

    all_logs = []
    for block in range(start_block, end_block + 1, batch_size):
        batch_end_block = min(block + batch_size - 1, end_block)
        events = contract.events[event].get_logs(
            fromBlock=block, toBlock=batch_end_block
        )
        all_logs += [event.args for event in events]

    logs = all_logs
    if receiver_address:
        if logs[0].get("to") != None:
            logs = [
                log for log in logs if log["to"].lower() == receiver_address.lower()
            ]
    if sender_address:
        if logs[0].get("from") != None:
            logs = [
                log for log in logs if log["from"].lower() == sender_address.lower()
            ]
    if tokenId:
        if logs[0].get("id") != None:
            logs = [log for log in logs if log["id"] == tokenId]

    return_object = EventResponse(event=event, data=logs)

    return return_object
