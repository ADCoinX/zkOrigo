from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import datetime, uuid, os

from chains import check_wallet
from ai_module import score_wallet
from zk_proof import generate_dummy_proof
from iso_export import generate_pain001_from_result
from rwa_module import generate_rwa_proof

app = FastAPI(title="zkOrigo - MVP")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")  # ✅ untuk download XML

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


@app.post("/api/rwa_proof")
async def rwa_api(payload: dict):
    asset = payload.get("asset", "UnknownAsset")
    reserve = float(payload.get("reserve", 0))
    supply = float(payload.get("supply", 0))
    return generate_rwa_proof(asset, reserve, supply)


async def run_validation(chain: str, address: str):
    # 1. Chain call
    chain_result = await check_wallet(chain, address)
    balance = chain_result.get("balance", "0")

    # 2. AI scoring
    ai_result = score_wallet(chain, address, chain_result)

    # 3. Proof ID + timestamp
    proof_id = f"zkorigo-{uuid.uuid4().hex[:12]}"
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"

    # 4. Build result
    result = {
        "chain": chain,
        "wallet": address,
        "balance": balance,
        "risk_score": ai_result["risk_score"],
        "ai_reason": ai_result["reasons"],
        "ai_version": ai_result["version"],
        "timestamp": timestamp,
        "proof_id": proof_id,
    }

    # 5. Add zkProof + ISO XML
    result["zk_proof"] = generate_dummy_proof(result)

    # Generate ISO XML string
    xml_str = generate_pain001_from_result(result)

    # Save XML file
    os.makedirs("outputs", exist_ok=True)
    filename = f"outputs/{proof_id}.xml"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(xml_str)

    result["iso_xml"] = xml_str
    result["xml_path"] = filename  # ✅ untuk template download

    # 6. Update stats
    STATS["total_proofs"] += 1
    STATS["unique_wallets"].add(address)
    STATS["by_chain"][chain] = STATS["by_chain"].get(chain, 0) + 1

    return result


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)
