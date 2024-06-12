import os
from dotenv import load_dotenv


class PrivateKeyService:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Initialize a dictionary to store private keys loaded from environment variables
        self.private_keys = {
            "0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73": os.getenv("0xFE3B557E8Fb62b89F4916B721be55cEb828dBd73"),
            "0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844": os.getenv("0x2DFc6e58d8a388cE38b5413ca2458a7b59d1B844"),
            "0x9F6C344071C0FDf43132eEfA8309a770A063D82D": os.getenv("0x9F6C344071C0FDf43132eEfA8309a770A063D82D"),
            "0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6": os.getenv("0x0b97F7B3FC38bF1DFf740d65B582c61b3E84FfC6"),
            "0x03B950EC5b1D893CDEB5d9A8A9165FeC3eF7914e": os.getenv("0x03B950EC5b1D893CDEB5d9A8A9165FeC3eF7914e"),
            "0x3DEFCA6A535B57570505952a9f0aA59F83ac0125": os.getenv("0x3DEFCA6A535B57570505952a9f0aA59F83ac0125"),
            "0x9AC65C5FF92e9C52fA342fA9D8e681637A4C80e0": os.getenv("0x9AC65C5FF92e9C52fA342fA9D8e681637A4C80e0"),
            "0x63F3D8fA9Bad9E6f6177530F18dA0500088eD087": os.getenv("0x63F3D8fA9Bad9E6f6177530F18dA0500088eD087"),
        }

    def get_private_key(self, wallet_address: str):
        # Check if the private key is in the list
        if wallet_address in self.private_keys.keys():
            return self.private_keys[wallet_address]
        else:
            raise Exception("Wallet address not found")
