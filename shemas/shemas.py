from pydantic import BaseModel


class Example(BaseModel):
    name: str
    song: str