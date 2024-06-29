from service.blockchain_service import BlockchainService


class RoleService:

    def __init__(self):
        self.blockchainService = BlockchainService()
        self.web3 = self.blockchainService.get_web3()
        self.contract = self.blockchainService.get_contract()
        self.chain_id = self.blockchainService.get_chain_id()

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

        tnx_receit = self.blockchainService.sign_and_send_txn(from_wallet, txn_dict)
        return tnx_receit
