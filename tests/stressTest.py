from locust import HttpUser, task, between, events
import random

from threading import Lock


class SafeTokenDict:
    def __init__(self):
        self.token_dict = {
            "sheep_token": [],
            "cow_token": [],
            "sheep_carcass_token": [],
            "cow_carcass_token": [],
            "sheep_demi_carcass_token": [],
            "cow_demi_carcass_token": [],
            "meat_token": [],
        }
        self.lock = Lock()

    def append_token(self, token_type, token_id):
        with self.lock:
            if token_type in self.token_dict:
                self.token_dict[token_type].append(token_id)
                print(f"Appended {token_id} to {token_type}")  # For debugging
            else:
                print(f"Token type {token_type} not found")

    def __getitem__(self, key):
        with self.lock:
            return self.token_dict[key]


class StressTest(HttpUser):
    wait_time = between(1, 4)
    token_dict = SafeTokenDict()

    admin_wallet_address = "0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73"

    wallet_addresses = {
        "BREEDER": "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844",
        "SLAUGHTERER": "0x9F6C344071C0FDf43132eEfA8309a770A063D82D",
        "MANUFACTURER": "0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6",
    }

    def on_start(self):
        for role, wallet_address in self.wallet_addresses.items():
            data = {
                "from_wallet_address": self.admin_wallet_address,
                "target_wallet_address": wallet_address,
                "role": role,
            }
            headers = {"Content-Type": "application/json"}
            self.client.post("/roles/assignRole", json=data, headers=headers)

    @task
    def get_metadata(self):
        print("Getting metaData")
        print(self.token_dict.token_dict)
        all_tokens = (
            self.token_dict["sheep_token"]
            + self.token_dict["cow_token"]
            + self.token_dict["sheep_carcass_token"]
            + self.token_dict["cow_carcass_token"]
            + self.token_dict["sheep_demi_carcass_token"]
            + self.token_dict["cow_demi_carcass_token"]
            + self.token_dict["meat_token"]
        )

        if len(all_tokens) == 0:
            return
        tokenId = random.choice(all_tokens)
        self.client.get(
            f"/resource/{tokenId}/metadata?recursive=true",
            name="/resource/[tokenId]/metadata",
        )

    @task
    def get_resource_by_wallet(self):
        print("Getting resource by wallet")
        wallet_address = random.choice(list(self.wallet_addresses.values()))

        metaData = random.choice([True, False])
        recursive = random.choice([True, False])

        self.client.get(
            f"/resource/{wallet_address}?metaData={metaData}&recursive={recursive}",
            name="/resource/[wallet_address]",
        )

    @task
    def set_meta_data(self):
        print("Setting metaData")
        all_tokens = (
            self.token_dict["sheep_token"]
            + self.token_dict["cow_token"]
            + self.token_dict["sheep_carcass_token"]
            + self.token_dict["cow_carcass_token"]
            + self.token_dict["sheep_demi_carcass_token"]
            + self.token_dict["cow_demi_carcass_token"]
            + self.token_dict["meat_token"]
        )

        if len(all_tokens) == 0:
            return
        tokenId = random.choice(all_tokens)
        payload = {
            "from_wallet_address": self.admin_wallet_address,
            "tokenId": tokenId,
            "metaData": {
                "key": "value",
                "key2": "value2",
                "key3": {"key": "value", "key2": "value2", "key3": "value3"},
                "key4": "asfasfdasfasfdasfdasfdasdfasdfasdfasfdsadfsadfasfdasdfasfdasfsfasfdasfd",
                "key5": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            },
        }

        headers = {"Content-Type": "application/json"}
        self.client.post("/resource/metaData", json=payload, headers=headers)

    @task
    def mint_sheep_or_cow(self):
        print("Minting sheep or cow")

        payload = {
            "from_wallet_address": self.wallet_addresses["BREEDER"],
            "resourceId": 42,
            "quantity": 1,
            "metaData": {"key": "value"},
            "ingredients": [],
        }

        headers = {"Content-Type": "application/json"}
        response = self.client.post("/resource/mint", json=payload, headers=headers)
        token_id = response.json()["tokenId"]
        self.token_dict.append_token("sheep_token", token_id)

        payload = {
            "from_wallet_address": self.wallet_addresses["BREEDER"],
            "resourceId": 43,
            "quantity": 1,
            "metaData": {"key": "value"},
            "ingredients": [],
        }

        headers = {"Content-Type": "application/json"}
        response = self.client.post("/resource/mint", json=payload, headers=headers)
        token_id = response.json()["tokenId"]
        self.token_dict.append_token("cow_token", token_id)

        print(self.token_dict.token_dict)

        if (
            len(self.token_dict["sheep_token"]) > 0
            and len(self.token_dict["cow_token"]) > 0
        ):
            # transfer sheep
            payload = {
                "tokenId": self.token_dict["sheep_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["BREEDER"],
                "to_wallet_address": self.wallet_addresses["SLAUGHTERER"],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

            # transfer cow
            payload = {
                "tokenId": self.token_dict["cow_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["BREEDER"],
                "to_wallet_address": self.wallet_addresses["SLAUGHTERER"],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

    @task
    def create_carcass(self):
        print("Creating carcass")
        if (
            len(self.token_dict["sheep_token"]) > 0
            and len(self.token_dict["cow_token"]) > 0
        ):
            # slaughter sheep
            payload = {
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "resourceId": 45,
                "quantity": 1,
                "metaData": {"key": "value"},
                "ingredients": [self.token_dict["sheep_token"].pop()],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post("/resource/mint", json=payload, headers=headers)
            self.token_dict.append_token(
                "sheep_carcass_token", response.json()["tokenId"]
            )

            # slaughter cow
            payload = {
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "resourceId": 46,
                "quantity": 1,
                "metaData": {"key": "value"},
                "ingredients": [self.token_dict["cow_token"].pop()],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post("/resource/mint", json=payload, headers=headers)
            self.token_dict.append_token(
                "cow_carcass_token", response.json()["tokenId"]
            )

        if (
            len(self.token_dict["sheep_carcass_token"]) > 0
            and len(self.token_dict["cow_carcass_token"]) > 0
        ):
            # transfer sheep
            payload = {
                "tokenId": self.token_dict["sheep_carcass_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["BREEDER"],
                "to_wallet_address": self.wallet_addresses["SLAUGHTERER"],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

            # transfer cow
            payload = {
                "tokenId": self.token_dict["cow_carcass_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["BREEDER"],
                "to_wallet_address": self.wallet_addresses["SLAUGHTERER"],
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

        print(self.token_dict.token_dict)

    @task
    def create_demi_carcasses(self):
        print("Creating demi carcasses")
        if (
            len(self.token_dict["sheep_carcass_token"]) > 0
            and len(self.token_dict["cow_carcass_token"]) > 0
        ):
            # create sheep demi carcass
            payload = {
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "producer_token_id": self.token_dict["sheep_carcass_token"].pop(),
                "metaData": {"key": "value"},
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/mintToMany", json=payload, headers=headers
            )
            for response_json in response.json():
                self.token_dict.append_token(
                    "sheep_demi_carcass_token", response_json["tokenId"]
                )

            # create cow demi carcass
            payload = {
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "producer_token_id": self.token_dict["cow_carcass_token"].pop(),
                "metaData": {"key": "value"},
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/mintToMany", json=payload, headers=headers
            )
            for response_json in response.json():
                self.token_dict.append_token(
                    "cow_demi_carcass_token", response_json["tokenId"]
                )

        if (
            len(self.token_dict["sheep_demi_carcass_token"]) > 0
            and len(self.token_dict["cow_demi_carcass_token"]) > 0
        ):
            # transfer sheep demi carcass
            payload = {
                "tokenId": self.token_dict["sheep_demi_carcass_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "to_wallet_address": self.wallet_addresses["MANUFACTURER"],
            }
            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

            # transfer cow demi carcass
            payload = {
                "tokenId": self.token_dict["cow_demi_carcass_token"][-1],
                "quantity": 1,
                "from_wallet_address": self.wallet_addresses["SLAUGHTERER"],
                "to_wallet_address": self.wallet_addresses["MANUFACTURER"],
            }
            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/transfer", json=payload, headers=headers
            )

        print(self.token_dict.token_dict)

    @task
    def create_meat(self):
        print("Creating meat")
        if (
            len(self.token_dict["sheep_demi_carcass_token"]) > 0
            and len(self.token_dict["cow_demi_carcass_token"]) > 0
        ):

            # create sheep meat
            payload = {
                "from_wallet_address": self.wallet_addresses["MANUFACTURER"],
                "producer_token_id": self.token_dict["sheep_demi_carcass_token"].pop(),
                "metaData": {"key": "value"},
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/mintToMany", json=payload, headers=headers
            )
            for response_json in response.json():
                self.token_dict.append_token("meat_token", response_json["tokenId"])

            # create cow meat
            payload = {
                "from_wallet_address": self.wallet_addresses["MANUFACTURER"],
                "producer_token_id": self.token_dict["cow_demi_carcass_token"].pop(),
                "metaData": {"key": "value"},
            }

            headers = {"Content-Type": "application/json"}
            response = self.client.post(
                "/resource/mintToMany", json=payload, headers=headers
            )
            for response_json in response.json():
                self.token_dict.append_token("meat_token", response_json["tokenId"])

        print(self.token_dict.token_dict)
