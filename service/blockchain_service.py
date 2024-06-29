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

        self.chain_id = 1337

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

    def get_available_roles(self):
        resources = self.contract.functions.getResourceTemplates().call()
        return list(set([resource[5] for resource in resources]))

    def get_role_of(self, wallet_address):
        if not self.web3.is_address(wallet_address):
            raise Exception("Invalid wallet address")
        roles = self.contract.functions.userRoles(wallet_address).call()
        return roles

    def assign_role_to_user(self, from_wallet_private_key, target_wallet_address, role):
        from_wallet = self.web3.eth.account.from_key(from_wallet_private_key)
        if not self.web3.is_address(from_wallet.address):
            raise Exception("Invalid wallet address")
        if not self.web3.is_address(target_wallet_address):
            raise Exception("Invalid wallet address")

        txn_dict = self.contract.functions.giveUserRole(
            target_wallet_address, role
        ).build_transaction(
            {
                "from": from_wallet.address,
                "chainId": self.chain_id,
                "nonce": self.web3.eth.get_transaction_count(from_wallet.address),
            }
        )

        tnx_receit = self._sign_and_send_txn(from_wallet, txn_dict)
        return tnx_receit

    def _sign_and_send_txn(self, from_wallet, txn_dict):
        signed_txn = self.web3.eth.account.sign_transaction(
            txn_dict, private_key=from_wallet.key
        )
        txn_hash = self.web3.eth.send_raw_transaction(signed_txn.rawTransaction)
        txn_receipt = self.web3.eth.wait_for_transaction_receipt(txn_hash)
        return txn_receipt

    def get_events(self, event):
        start_block = 0
        end_block = self.web3.eth.block_number
        batch_size = 1000

        all_logs = []
        for block in range(start_block, end_block + 1, batch_size):
            batch_end_block = min(block + batch_size - 1, end_block)
            events = self.contract.events[event].get_logs(
                fromBlock=block, toBlock=batch_end_block
            )
            all_logs += [event.args for event in events]

        return all_logs
