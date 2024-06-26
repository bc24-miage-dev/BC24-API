import json
from web3 import Web3
from web3.middleware import geth_poa_middleware
from core.config import contract_settings
from shemas.Data import Data
from shemas.MetaData import MetaData


class BlockchainService:
    def __init__(self):
        self.web3 = Web3(Web3.HTTPProvider(contract_settings.validator_address))
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

        self.contract = self.web3.eth.contract(
            address=contract_settings.contract_address,
            abi=contract_settings.contract_abi,
        )

        self.chain_id = 1337

    def get_web3(self):
        return self.web3

    def get_contract(self):
        return self.contract

    def get_chain_id(self):
        return self.chain_id

    def sign_and_send_txn(self, from_wallet, txn_dict):
        signed_txn = self.web3.eth.account.sign_transaction(
            txn_dict, private_key=from_wallet.key
        )
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        return txn_receipt
