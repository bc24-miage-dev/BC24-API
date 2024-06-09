import json
from pathlib import Path


class GlobalConfig:  
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
    
    validator_address: str = "https://validator3.rpc.bc24.miage.dev"
    contract_address: str = "0x42699A7612A82f1d9C36148af9C77354759b210b"
    contract_abi = json.load((Path(__file__).parent / "abi.json").open())
  
contract_settings = ContractConfig()