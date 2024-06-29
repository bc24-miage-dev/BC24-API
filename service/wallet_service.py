from service.blockchain_service import BlockchainService


class WalletService:

    def __init__(self):
        blockchainService = BlockchainService()
        self.web3 = blockchainService.get_web3()

    def create_wallet(self):
        acc = self.web3.eth.account.create()
        return acc.address, self.web3.to_hex(acc.key)

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

        return self.web3.to_hex(txn_hash)
