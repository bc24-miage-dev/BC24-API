from fastapi import APIRouter, HTTPException, status
from shemas.shemas import RoleAssignment
from core.config import contract_settings
from web3.middleware import geth_poa_middleware
from web3 import Web3

# Connect to the blockchain
web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = web3.eth.contract(
    address=contract_settings.contract_address, abi=contract_settings.contract_abi)


router = APIRouter()


@router.post("/assign-role")
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


@router.get("/test_mint")
async def test():
    # Get account form private key
    account = web3.eth.account.from_key(
        "99f55cdda1001d13735212a7cd2944f12460046f8c26c17d784ccaa0042eeb62")

    # Function parameters
    resourceId = 1  # Example resourceId
    quantity = 1  # Example quantity
    _metaData = "Example metadata"  # Example metadata
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

    # print(resource_created_events[0].args)

    return resource_created_events[0].args


@router.get("/ResourceCreatedEvents")
async def ResourceCreatedEvents():
    # Testing the event filters
    last_event = contract.events.ResourceCreatedEvent.get_logs(fromBlock=1)[
        0].args

    return {"Event": last_event}


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
