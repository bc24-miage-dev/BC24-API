from fastapi import APIRouter
from web3 import Web3
from web3.middleware import geth_poa_middleware

from core.config import contract_settings
from service.private_key_service import PrivateKeyService

from api.routes.wallet_routes import router as wallet_router
from api.routes.roles_routes import router as roles_router
from api.routes.event_routes import router as event_router
from api.routes.resource_routes import router as resource_router

web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

contract = web3.eth.contract(
    address=contract_settings.contract_address, abi=contract_settings.contract_abi
)

private_key_service = PrivateKeyService()


router = APIRouter()
router.include_router(wallet_router)
router.include_router(roles_router)
router.include_router(event_router)
router.include_router(resource_router)
