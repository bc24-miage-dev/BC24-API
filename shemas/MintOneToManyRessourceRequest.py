from pydantic import BaseModel

class MintOneToManyRessourceRequest(BaseModel):
    from_wallet_address: str
    producer_token_id: int
    metaData: dict
