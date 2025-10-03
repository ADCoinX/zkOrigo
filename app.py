from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import datetime, uuid

from chains import check_wallet
from ai_module import run_ai_scoring
from zk_proof import generate_dummy_proof
from iso_export import generate_pain001_from_result

app = FastAPI(title="zkOrigo - MVP")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple stats counter
STATS = {"total_proofs": 0, "unique_wallets": set(), "by_chain": {}}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/validate", response_class=HTMLResponse)
async def validate_form(request: Request, chain: str = Form(...), address: str = Form(...)):
    result = await run_validation(chain, address)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})

@app.post("/api/validate")
async def validate_api(payload: dict):
    chain = payload.get("chain")
    address = payload.get("address")
    if not chain or not address:
        raise HTTPException(status_code=400, detail="chain and address required")
    return await run_validation(chain, address)

@app.get("/api/stats")
async def get_stats():
    return {
        "total_proofs": STATS["total_proofs"],
        "unique_wallets": len(STATS["unique_wallets"]),
        "by_chain": STATS["by_chain"]
    }

async def run_validation(chain: str, address: str):
    # 1. Chain call (dummy fallback)
    chain_result = await check_wallet(chain, address)

    # 2. AI scoring
    risk_score, reasons = run_ai_scoring(chain, address, chain_result)

    # 3. Proof ID + hash
    proof_id = f"zkorigo-{uuid.uuid4().hex[:12]}"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    result = {
        "chain": chain,
        "wallet": address,
        "risk_score": risk_score,
        "ai_reason": reasons,
        "ai_version": "heuristic-v1",
        "timestamp": timestamp,
        "proof_id": proof_id
    }
    result["zk_proof"] = generate_dummy_proof(result)
    result["iso_xml"] = generate_pain001_from_result(result)

    # 4. Update stats
    STATS["total_proofs"] += 1
    STATS["unique_wallets"].add(address)
    STATS["by_chain"][chain] = STATS["by_chain"].get(chain, 0) + 1

    return result

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)
