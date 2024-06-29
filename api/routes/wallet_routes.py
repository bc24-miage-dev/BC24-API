from fastapi import APIRouter, HTTPException

from service.blockchain_service import BlockchainService
from service.private_key_service import PrivateKeyService
from service.wallet_service import WalletService
from shemas.CreateWalletResponse import CreateWalletResponse
from shemas.TransactionRequest import TransactionRequest
from shemas.TransactionResponse import TransactionResponse

wallet_service = WalletService()
private_key_service = PrivateKeyService()

router = APIRouter(
    prefix="/wallet",
    tags=["wallet"],
)


@router.get("/create", response_model=CreateWalletResponse)
async def create_wallet():
    try:
        wallet_address, wallet_key = wallet_service.create_wallet()
        private_key_service.add_private_key(wallet_address, wallet_key)
        return CreateWalletResponse(wallet_address=wallet_address)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/static", response_model=CreateWalletResponse)
async def create_wallet():

    return CreateWalletResponse(
        wallet_address="0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6"
    )


@router.post(
    "/send-eth",
    response_model=TransactionResponse,
    responses={404: {"description": "Sender address not found"}},
)
async def send_eth(transaction_request: TransactionRequest):
    sender_address = transaction_request.sender_address
    receiver_address = transaction_request.receiver_address
    amount_in_ether = transaction_request.amount

    # Retrieve the private key securely
    try:
        private_key = private_key_service.get_private_key(sender_address)
    except KeyError:
        raise HTTPException(status_code=404, detail="Sender address not found")

    transaction = wallet_service.send_eth(
        sender_address, receiver_address, amount_in_ether, private_key
    )

    return TransactionResponse(
        transaction_hash=transaction, details="ETH sent successfully"
    )
