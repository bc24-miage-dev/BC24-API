import os
from dotenv import load_dotenv
import re

class PrivateKeyService:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        with open('.env', 'r') as file:
            content = file.read()

        addresses = re.findall(r'0x[a-fA-F0-9]{40}', content)

        self.private_keys = {}
        for address in addresses:
            if address not in self.private_keys:
                self.private_keys[address] = os.getenv(address)

    def get_private_key(self, wallet_address: str):
        # Check if the private key is in the list
        if wallet_address in self.private_keys.keys():
            return self.private_keys[wallet_address]
        else:
            raise Exception("Wallet address not found")
        
    
    def add_private_key(self,account, key):
        self.private_keys[account] = key
        with open('.env', 'a') as env_file:
            # Format the string to be written
            env_entry = f"{account}={key}\n"
            # Write the formatted string to the .env file
            env_file.write(env_entry)
