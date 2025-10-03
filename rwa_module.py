import hashlib, json, datetime

def generate_rwa_proof(asset_name: str, reserve_amount: float, token_supply: float):
    """
    Dummy RWA zkProof generator
    """
    timestamp = datetime.datetime.utcnow().isoformat() + "Z"
    verified = reserve_amount >= token_supply

    payload = {
        "asset": asset_name,
        "reserve_amount": reserve_amount,
        "token_supply": token_supply,
        "verified": verified,
        "timestamp": timestamp
    }

    s = json.dumps(payload, sort_keys=True).encode()
    h = hashlib.sha256(s).hexdigest()

    return {
        "proof_id": f"rwa-{h[:12]}",
        "zk_proof": f"dummy-rwa-sha256:{h}",
        **payload
    }
