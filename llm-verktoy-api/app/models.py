from pydantic import BaseModel
from typing import List

class Konsulent(BaseModel):
    id: int
    navn: str
    ferdigheter: List[str]
    belastning_prosent: int

class SammendragRespons(BaseModel):
    sammendrag: str

