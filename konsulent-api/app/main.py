from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI(title="konsulent-api")

class Konsulent(BaseModel):
    id: int
    navn: str
    ferdigheter: List[str]
    belastning_prosent: int

KONSULENTER = [
    Konsulent(id=1, navn="Mads Hagberg.", ferdigheter=["python", "fastapi", "azure"], belastning_prosent=40),
    Konsulent(id=2, navn="Linus Torvald.", ferdigheter=["c++", "aws", "sql"], belastning_prosent=10),
    Konsulent(id=3, navn="ilya sutseker", ferdigheter=["java", "kotlin", "spring"], belastning_prosent=70),
    Konsulent(id=4, navn="Hedda Gabler.", ferdigheter=["react", "typescript"], belastning_prosent=45),
    Konsulent(id=5, navn="Clark Kent.", ferdigheter=["ruby", ".Net", "java"], belastning_prosent=90), 
]

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/konsulenter", response_model=List[Konsulent])
def get_konsulenter():
    return KONSULENTER

