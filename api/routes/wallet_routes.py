from fastapi import APIRouter, HTTPException

from service.blockchain_service import BlockchainService
from service.walletService import PrivateKeyService
from shemas.CreateWalletResponse import CreateWalletResponse
from shemas.TransactionRequest import TransactionRequest
from shemas.TransactionResponse import TransactionResponse

blockchainSerivce = BlockchainService()
web3 = blockchainSerivce.web3

private_key_service = PrivateKeyService()

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@router.get("/create", response_model=CreateWalletResponse)
async def create_wallet():
    try:
        acc = web3.eth.account.create()
        private_key_service.add_private_key(acc.address, web3.to_hex(acc.key))

        return CreateWalletResponse(wallet_address=acc.address)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/static", response_model=CreateWalletResponse)
async def create_wallet():

    return CreateWalletResponse("0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6")


@router.post(
    "/send-eth",
    response_model=TransactionResponse,
    responses={404: {"description": "Sender address not found"}},
)
async def send_eth(transaction_request: TransactionRequest):
    sender_address = transaction_request.sender_address
    receiver_address = transaction_request.receiver_address
    amount_in_ether = transaction_request.amount
    amount_in_wei = web3.to_wei(amount_in_ether, "ether")

    # Retrieve the private key securely
    try:
        private_key = private_key_service.get_private_key(sender_address)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sender address not found")

    # Build and sign the transaction
    nonce = web3.eth.get_transaction_count(sender_address)
    txn = {
        "nonce": nonce,
        "to": receiver_address,
        "value": amount_in_wei,
        "gas": 2000000,
        "gasPrice": web3.to_wei("50", "gwei"),
    }
    signed_txn = web3.eth.account.sign_transaction(txn, private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    txn_hash_hex = web3.to_hex(txn_hash)

    return TransactionResponse(
        transaction_hash=txn_hash_hex, details="ETH sent successfully"
    )
