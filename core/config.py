import json
from pathlib import Path
import os
from dotenv import load_dotenv


class GlobalConfig:  

    
    load_dotenv()
    def __init__(self):  
        pass  
  
    title: str = "BC24-API"  
    version: str = "0.1.0"  
    description: str = "API for BC24 Tracability project"  
    openapi_prefix: str = ""  
    docs_url: str = "/docs"  
    redoc_url: str = "/redoc"  
    openapi_url: str = "/openapi.json"  
    api_prefix: str = ""

settings = GlobalConfig()

class ContractConfig:  
    def __init__(self):  
        pass  
    
    validator_address: str = os.getenv("VALIDATOR_URL")
    contract_address: str = os.getenv("CONTRACT_ADDRESS")
    contract_abi = json.load((Path(__file__).parent / "abi.json").open())
  
contract_settings = ContractConfig()