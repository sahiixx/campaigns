#!/usr/bin/env python3
"""Campaign API Gateway — Unified entry point for all backends."""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import httpx

app = FastAPI(title="Campaign Gateway")

SERVICES = {
    "ghost": "http://localhost:8000",
    "dubai": "http://localhost:8002",
    "gumroad": "http://localhost:8003",
    "telegram": "http://localhost:8004",
    "crm": "http://localhost:8005",
}

@app.get("/")
def home():
    return {"gateway": "Campaign API Gateway", "services": list(SERVICES.keys())}

@app.get("/health")
async def health():
    status = {}
    async with httpx.AsyncClient(timeout=5) as client:
        for name, url in SERVICES.items():
            try:
                r = await client.get(f"{url}/")
                status[name] = {"status": "up", "code": r.status_code}
            except Exception as e:
                status[name] = {"status": "down", "error": str(e)}
    return status

@app.get("/stats")
async def stats():
    data = {}
    async with httpx.AsyncClient(timeout=5) as client:
        for name, url in SERVICES.items():
            try:
                if name == "ghost":
                    r = await client.get(f"{url}/appointments")
                    data[name] = {"appointments": len(r.json())}
                elif name == "dubai":
                    r = await client.get(f"{url}/viewings")
                    data[name] = {"viewings": len(r.json())}
                elif name == "crm":
                    r = await client.get(f"{url}/stats")
                    data[name] = r.json()
                elif name == "gumroad":
                    r = await client.get(f"{url}/")
                    data[name] = r.json().get("stats", {})
                else:
                    data[name] = {"status": "active"}
            except Exception as e:
                data[name] = {"error": str(e)}
    return data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006)
