import hashlib, json

def generate_dummy_proof(result: dict) -> str:
    payload = {
        "wallet": result.get("wallet"),
        "chain": result.get("chain"),
        "risk_score": result.get("risk_score"),
        "timestamp": result.get("timestamp")
    }
    s = json.dumps(payload, sort_keys=True).encode()
    h = hashlib.sha256(s).hexdigest()
    return f"dummy-sha256:{h}"
