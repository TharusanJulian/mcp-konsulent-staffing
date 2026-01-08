import httpx
from typing import List
from .models import Konsulent

async def hent_konsulenter(base_url: str) -> List[Konsulent]:
    async with httpx.AsyncClient(base_url=base_url, timeout=5.0) as client:
        resp = await client.get("/konsulenter")
        resp.raise_for_status()
        data = resp.json()
        return [Konsulent(**k) for k in data]

