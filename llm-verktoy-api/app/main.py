from fastapi import FastAPI, HTTPException, Query
from typing import List, Tuple
import os

from .models import SammendragRespons, Konsulent
from .client import hent_konsulenter

app = FastAPI(title="llm-verktoy-api")

KONSULENT_API_URL = os.getenv("KONSULENT_API_URL", "http://konsulent-api:8000")

@app.get("/health")
def health():
    return {"status": "ok"}

def beregn_tilgjengelighet(k: Konsulent) -> int:
    return max(0, min(100, 100 - k.belastning_prosent))

def filtrer_konsulenter(
    konsulenter: List[Konsulent],
    min_tilgjengelighet_prosent: int,
    paakrevd_ferdighet: str,
) -> List[Tuple[Konsulent, int]]:
    ferdighet = paakrevd_ferdighet.lower()
    resultat = []

    for k in konsulenter:
        tilgjengelighet = beregn_tilgjengelighet(k)
        ferdigheter_lower = [f.lower() for f in k.ferdigheter]

        if tilgjengelighet >= min_tilgjengelighet_prosent and ferdighet in ferdigheter_lower:
            resultat.append((k, tilgjengelighet))

    return resultat

def lag_sammendrag(
    filtrerte: List[Tuple[Konsulent, int]],
    min_tilgjengelighet_prosent: int,
    paakrevd_ferdighet: str,
) -> str:
    antall = len(filtrerte)
    ordet = "konsulent" if antall == 1 else "konsulenter"

    if antall == 0:
        return (
            f"Fant 0 konsulenter med minst {min_tilgjengelighet_prosent}% "
            f"tilgjengelighet og ferdigheten '{paakrevd_ferdighet}'."
        )

    deler = [
        f"Fant {antall} {ordet} med minst {min_tilgjengelighet_prosent}% "
        f"tilgjengelighet og ferdigheten '{paakrevd_ferdighet}'."
    ]

    for k, tilgjengelighet in filtrerte:
        deler.append(f"{k.navn} har {tilgjengelighet}% tilgjengelighet.")

    return " ".join(deler)

@app.get("/tilgjengelige-konsulenter/sammendrag", response_model=SammendragRespons)
async def tilgjengelige_konsulenter_sammendrag(
    min_tilgjengelighet_prosent: int = Query(..., ge=0, le=100),
    paakrevd_ferdighet: str = Query(..., min_length=1),
):
    try:
        konsulenter = await hent_konsulenter(KONSULENT_API_URL)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Feil mot konsulent-api: {e}")

    filtrerte = filtrer_konsulenter(konsulenter, min_tilgjengelighet_prosent, paakrevd_ferdighet)
    sammendrag = lag_sammendrag(filtrerte, min_tilgjengelighet_prosent, paakrevd_ferdighet)
    return SammendragRespons(sammendrag=sammendrag)

