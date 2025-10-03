import hashlib, json, time

def generate_dummy_proof(result: dict) -> str:
    # Deterministic dummy proof: SHA256 of selected fields
    payload = {
        "wallet": result.get("wallet"),
        "chain": result.get("chain"),
        "risk_score": result.get("risk_score"),
        "timestamp": result.get("timestamp")
    }
    s = json.dumps(payload, sort_keys=True).encode()
    h = hashlib.sha256(s).hexdigest()
    # prefix to indicate dummy proof (clear for reviewers)
    return f"dummy-sha256:{h}"
