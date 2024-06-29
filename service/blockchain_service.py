from web3 import Web3
from web3.middleware import geth_poa_middleware
from core.config import contract_settings


class BlockchainService:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.contract = self.web3.eth.contract(
            address=contract_settings.contract_address,
            abi=contract_settings.contract_abi,
        )
