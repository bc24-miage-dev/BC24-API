from locust import HttpUser, task, between, events
import random


class StressTest(HttpUser):
    wait_time = between(1, 4)
    wallet_addresses = [
        "0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73",
        "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
        "0x9F6C344071C0FDf43132eEfA8309a770A063D82D",
        "0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6",
        "0x03B950EC5b1D893CDEB5d9A8A9165FeC3eF7914e",
        "0x3DEFCA6A535B57570505952a9f0aA59F83ac0125",
        "0x9AC65C5FF92e9C52fA342fA9D8e681637A4C80e0",
        "0x63F3D8fA9Bad9E6f6177530F18dA0500088eD087"]

    @task
    def get_metadata(self):
        tokenId = random.randint(1, 100)
        self.client.get(
            f"/resource/{tokenId}/metadata?recursive=true", name="/resource/[tokenId]/metadata")

    @task
    def get_resource_by_wallet(self):

        wallet_address = random.choice(self.wallet_addresses)

        metaData = random.choice([True, False])
        recursive = random.choice([True, False])

        self.client.get(
            f"/resource/{wallet_address}?metaData={metaData}&recursive={recursive}", name="/resource/[wallet_address]")

    @task
    def only_mint_resource(self):
        # only breeder for now
        payload = {
            "wallet_address": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
            "resourceId": 1,
            "quantity": 1,
            "metaData": {"key": "value"},
            "ingredients": []
        }
        headers = {'Content-Type': 'application/json'}
        self.client.post("/resource/mint", json=payload, headers=headers)

    @task
    def mint_and_change_resource(self):
        payload = {
            "from_wallet_address": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
            "resourceId": 1,
            "quantity": 1,
            "metaData": {"key": "value"},
            "ingredients": []
        }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(
            "/resource/mint", json=payload, headers=headers)

        payload = {
            "from_wallet_address": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
            "tokenId": response.json()["tokenId"],
            "metaData": {"newKey": "newValue"}
        }

        headers = {'Content-Type': 'application/json'}
        self.client.post("/resource/metadata", json=payload, headers=headers)

    @task
    def mint_and_transfer_resource(self):
        # only breeder for now
        payload = {
            "from_wallet_address": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
            "resourceId": 1,
            "quantity": 1,
            "metaData": {"key": "value"},
            "ingredients": []
        }
        headers = {'Content-Type': 'application/json'}
        response = self.client.post(
            "/resource/mint", json=payload, headers=headers)

        payload = {
            "tokenId": response.json()["tokenId"],
            "quantity": 1,
            "from_wallet_address": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
            "to_wallet_address": "0x9F6C344071C0FDf43132eEfA8309a770A063D82D"
        }

        headers = {'Content-Type': 'application/json'}
        self.client.post("/resource/transfer", json=payload, headers=headers)
