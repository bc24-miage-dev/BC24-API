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