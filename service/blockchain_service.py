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

    def create_wallet(self):
        acc = self.web3.eth.account.create()
        return acc

    def send_eth(self, sender_address, receiver_address, amount_in_ether, private_key):
        amount_in_wei = self.web3.to_wei(amount_in_ether, "ether")
        nonce = self.web3.eth.get_transaction_count(sender_address)
        txn = {
            "nonce": nonce,
            "to": receiver_address,
            "value": amount_in_wei,
            "gas": 2000000,
            "gasPrice": self.web3.to_wei("50", "gwei"),
        }
        signed_txn = self.web3.eth.account.sign_transaction(txn, private_key)
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return txn_hash
