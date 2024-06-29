from service.blockchain_service import BlockchainService


class ResourceService:

    def __init__(self):
        self.blockchainService = BlockchainService()
        self.web3 = self.blockchainService.get_web3()
        self.contract = self.blockchainService.get_contract()
        self.chain_id = self.blockchainService.get_chain_id()

    def get_templates(self):
        return self.contract.functions.getResourceTemplates().call()

    def mint_resource(
        self, from_wallet_private_key, resource_id, quantity, meta_data, ingredients
    ):
        account = self.web3.eth.account.from_key(from_wallet_private_key)
        transaction = self.contract.functions.mintRessource(
            resource_id, quantity, meta_data, ingredients
        ).build_transaction(
            {
                "from": account.address,
                "chainId": self.chain_id,
                "gasPrice": self.web3.eth.gas_price,
                "nonce": self.web3.eth.get_transaction_count(account.address),
            }
        )

        txn_receipt = self.blockchainService.sign_and_send_txn(account, transaction)

        return txn_receipt
