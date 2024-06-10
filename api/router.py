import json
import random
from fastapi import APIRouter, HTTPException, status
from shemas.shemas import MetaData, MintToManyData, RoleAssignment
from core.config import contract_settings
from web3.middleware import geth_poa_middleware
from web3 import Web3

# Connect to the blockchain
web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = web3.eth.contract(
    address=contract_settings.contract_address, abi=contract_settings.contract_abi)


router = APIRouter()


@router.post("/assignRole")
async def assign_role(data: RoleAssignment):
    # Ensure the wallet address is valid
    if not web3.is_address(data.wallet_address):
        raise HTTPException(status_code=400, detail="Invalid wallet address")
    try:
        # Replace these with your account details
        account = web3.eth.account.from_key(
            "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63")

        # Prepare the transaction
        txn_dict = contract.functions.giveUserRole(data.wallet_address, data.role).build_transaction({
            "from": account.address,
            'chainId': 1337,  # Mainnet. Change accordingly if you're using a testnet
            'nonce': web3.eth.get_transaction_count(account.address),
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(
            txn_dict, private_key=account.key)

        # Send the transaction
        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")

    return {"status": "success", "transaction_hash": txn_receipt.transactionHash.hex()}


@router.get("/mintResource")
async def mint_resource():
    # Get account form private key
    account = web3.eth.account.from_key(
        "99f55cdda1001d13735212a7cd2944f12460046f8c26c17d784ccaa0042eeb62")

    data = {
        # Random weight between 50.0 and 100.0 kg
        "weight": round(random.uniform(50.0, 100.0), 2),
        "age": random.randint(18, 100),  # Random age between 18 and 100
        # Randomly choose between True (sick) and False (not sick)
        "sickness": random.choice([True, False]),
        # Random height between 150.0 and 200.0 cm
        "height": round(random.uniform(150.0, 200.0), 2),
        # Randomly choose a blood type
        "blood_type": random.choice(['A', 'B', 'AB', 'O']),
    }

    # Convert the dictionary to a JSON string
    json_data = json.dumps(data, indent=4)
    # Function parameters
    resourceId = 1  # Example resourceId
    quantity = 1  # Example quantity

    _metaData = json_data  # Example metadata
    ingredients = []  # Example ingredients

    # Build the transaction
    transaction = contract.functions.mintRessource(resourceId, quantity, _metaData, ingredients).build_transaction({
        "from": account.address,
        'chainId': 1337,
        "gasPrice": web3.eth.gas_price,
        "nonce": web3.eth.get_transaction_count(account.address),
    })

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(
        transaction, private_key=account.key)

    # Send the transaction

    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    # Extract and decode the 'ResourceCreatedEvent' from the transaction receipt
    resource_created_events = contract.events.ResourceCreatedEvent(
    ).process_receipt(txn_receipt)

    resource_metaDataEvent = contract.events.ResourceMetaDataChangedEvent(
    ).process_receipt(txn_receipt)

    # print(resource_created_events[0].args)

    return {resource_created_events[0].args, resource_metaDataEvent[0].args}

@router.post("/setMetaData")
async def set_metadata(data: MetaData):
    try:
        # Get account form private key
        account = web3.eth.account.from_key(
            "0x8f2a55949038a9610f50fb23b5883af3b4ecb3c3bb792cbcefbd1542c692be63")
        
        tokenId = data.tokenId
        _metaData = json.dumps(data.metaData, indent=4)

        transaction = contract.functions.setMetaData(tokenId, _metaData).build_transaction({
            "from": account.address,
            'chainId': 1337,
            "gasPrice": web3.eth.gas_price,
            "nonce": web3.eth.get_transaction_count(account.address),
        })

        # Sign the transaction
        signed_txn = web3.eth.account.sign_transaction(
            transaction, private_key=account.key)

        # Send the transaction

        txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for the transaction to be mined
        txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

        # Extract and decode the 'ResourceCreatedEvent' from the transaction receipt

        resource_metaDataEvent = contract.events.ResourceMetaDataChangedEvent(
        ).process_receipt(txn_receipt)
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=500, detail=f"Failed to send transaction: {e}")

    return {resource_metaDataEvent[0].args}

@router.post("/mintOneToMany")
async def mint_one_to_many(data: MintToManyData):
    return "to implement"

@router.get("/metadata/{tokenId}")
async def metadata(tokenId: int):
    try:
        # Call the contract function
        metadata = contract.functions.getMetaData(tokenId).call()
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to get metadata: {e}")

    return {"metadata": metadata}

@router.get("/events/{event}")
async def ResourceCreatedEvents(eventName: str):
    # Testing the event filters

    # Example setup
    start_block = 0
    end_block = web3.eth.block_number
    batch_size = 1000  # Adjust based on what your node can handle

    # Function to fetch logs in batches
    def fetch_logs_in_batches(contract, event, from_block, to_block, batch_size):
        logs = []
        for block in range(from_block, to_block + 1, batch_size):
            batch_end_block = min(block + batch_size - 1, to_block)
            logs.append(contract.events[eventName].get_logs(fromBlock=block, toBlock=batch_end_block))
    
    # iterate over the logs and append them to the list
            

    logs = fetch_logs_in_batches(contract, 'ResourceCreatedEvent', start_block, end_block, batch_size)

    """  last_event = contract.events.ResourceCreatedEvent.get_logs(fromBlock=1)[
        0].args """

    return {"Event": logs}


@router.get("/status/200")
async def status_200():
    return {"status": "OK"}


@router.get("/status/403")
async def status_403():
    raise HTTPException(status_code=403, detail="Forbidden")


@router.get("/status/404")
async def status_404():
    raise HTTPException(status_code=404, detail="Not Found")


@router.get("/status/500")
async def status_500():
    raise HTTPException(status_code=500, detail="Internal Server Error")
