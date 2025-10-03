from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
import json, hashlib, uuid, datetime
from iso_export import generate_pain001_from_result
from zk_proof import generate_dummy_proof

app = FastAPI(title="zkOrigo - MVP")

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple rate limiter placeholder (not production)
REQUEST_COUNTS = {}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})

@app.post("/validate", response_class=HTMLResponse)
async def validate_ui(request: Request, chain: str = Form(...), address: str = Form(...)):
    # Basic input validation
    chain = chain.lower()
    if not address:
        raise HTTPException(status_code=400, detail="Missing address")
    result = await run_validation(chain, address)
    xml_path = None
    if result.get("iso_xml"):
        # write xml to file for download
        fn = f"outputs/{result['proof_id']}.xml"
        Path("outputs").mkdir(exist_ok=True)
        with open(fn, "w", encoding="utf-8") as f:
            f.write(result["iso_xml"])
        xml_path = fn
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "xml_path": xml_path})

@app.post("/api/validate")
async def validate_api(payload: dict):
    chain = payload.get("chain")
    address = payload.get("address")
    api_key = payload.get("api_key")
    if not chain or not address:
        raise HTTPException(status_code=400, detail="chain and address required")
    # simple free tier throttling by IP simulated via payload.client_id (for demo)
    client = payload.get("client_id","public")
    count = REQUEST_COUNTS.get(client,0)
    if count > 1000:
        raise HTTPException(status_code=429, detail="rate limit exceeded")
    REQUEST_COUNTS[client] = count + 1
    result = await run_validation(chain.lower(), address)
    return result

async def run_validation(chain: str, address: str):
    # NOTE: This MVP uses dummy data and hash-based proof. Replace with real chain calls & ZK later.
    # Simple heuristic risk scoring
    score = 50
    reasons = []
    try:
        # heuristics
        if len(address) < 20:
            score += 20
            reasons.append("Short address (synthetic/legacy)")
        if address.lower().startswith("0x"):
            reasons.append("EVM-style address detected")
        # placeholder chain-specific tweak
        if chain in ("eth","polygon","bnb"):
            score += 5
        if chain in ("xrpl","xlm","hedera"):
            score += 2
        # timestamped id
        proof_id = f"zkorigo-{uuid.uuid4().hex[:12]}"
        # package result
        result = {
            "chain": chain,
            "wallet": address,
            "risk_score": max(0, min(100, score)),
            "ai_reason": reasons or ["Rule-based heuristic v1"],
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "ai_version": "heuristic-v1",
        }
        # generate dummy proof
        proof = generate_dummy_proof(result)
        result["zk_proof"] = proof
        result["proof_id"] = proof_id
        # generate ISO XML (pain.001) and attach
        iso_xml = generate_pain001_from_result(result)
        result["iso_xml"] = iso_xml
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=10000, reload=True)
