import json
from service.blockchain_service import BlockchainService
from shemas.Data import Data
from shemas.MetaData import MetaData


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

    def mint_one_to_many_resource(
        self, from_wallet_private_key, producer_token_id, meta_data
    ):
        account = self.web3.eth.account.from_key(from_wallet_private_key)

        transaction = self.contract.functions.mintOneToMany(
            producer_token_id, meta_data
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

    def transfer_resource(
        self,
        from_wallet_private_key,
        from_wallet_address,
        to_wallet_address,
        tokenId,
        quantity,
    ):

        if not self.web3.is_address(from_wallet_address):
            raise Exception("Invalid wallet address")
        if not self.web3.is_address(to_wallet_address):
            raise Exception("Invalid wallet address")

        account = self.web3.eth.account.from_key(from_wallet_private_key)

        txn_dict = self.contract.functions.safeTransferFrom(
            from_wallet_address,
            to_wallet_address,
            tokenId,
            quantity,
            b"",
        ).build_transaction(
            {
                "from": account.address,
                "chainId": self.chain_id,
                "nonce": self.web3.eth.get_transaction_count(account.address),
            }
        )

        txn_receipt = self.blockchainService.sign_and_send_txn(account, txn_dict)
        return txn_receipt

    def set_metadata(
        self, from_wallet_private_key, from_wallet_address, token_id, meta_data
    ):

        if not self.web3.is_address(from_wallet_address):
            raise Exception("Invalid wallet address")
        account = self.web3.eth.account.from_key(from_wallet_private_key)

        transaction = self.contract.functions.setMetaData(
            token_id, meta_data
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

    def get_enriched_metadata_of_tokens(self, token_ids, metaData, recursive):
        active_resources = []
        for token_id in token_ids:
            resource = {"tokenId": token_id, "balance": token_ids[token_id]}
            if metaData:
                enriched_metadata = self.fetch_and_enrich_metadata(token_id, recursive)
                resource = {**resource, "metaData": enriched_metadata}

            active_resources.append(resource)

        return active_resources

    def fetch_and_enrich_metadata(self, tokenId, recursive=True):
        metadata = self.contract.functions.getMetaData(tokenId).call()

        resource_metaData = metadata[0]
        resource_id = metadata[1]
        resource_name = metadata[2]
        resource_type = metadata[3]
        ingredients_token_ids = metadata[4]

        enriched_ingredients = []

        if recursive:
            for ingredient_tokenId in ingredients_token_ids:
                enriched_ingredient = self.fetch_and_enrich_metadata(ingredient_tokenId)
                enriched_ingredients.append(enriched_ingredient)
        else:
            enriched_ingredients = ingredients_token_ids

        transformed_metaData = [
            Data(
                required_role=data[0],
                stringData=json.loads(data[1]),
                lastModifiedBy=data[2],
                lastModifiedAt=data[3],
            )
            for data in resource_metaData
        ]

        return MetaData(
            data=transformed_metaData,
            resource_id=resource_id,
            resource_name=resource_name,
            resource_type=resource_type,
            ingredients=enriched_ingredients,
        )

    def get_balance_of_token(self, wallet_address, token_id):
        return self.contract.functions.balanceOf(wallet_address, token_id).call()
