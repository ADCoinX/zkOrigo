def run_ai_scoring(chain: str, address: str, chain_result: dict):
    score = 50
    reasons = []

    if len(address) < 20:
        score += 20
        reasons.append("Short address (synthetic/legacy)")

    if address.lower().startswith("0x"):
        reasons.append("EVM-style address detected")

    if chain in ("eth", "polygon", "bnb"):
        score += 5
        reasons.append("EVM chain (+5 risk)")

    if chain in ("xrpl", "xlm", "hedera"):
        score += 2
        reasons.append("Non-EVM chain (+2 risk)")

    if chain_result.get("error"):
        score += 10
        reasons.append("Endpoint error (chain fallback triggered)")

    return max(0, min(100, score)), reasons or ["Rule-based heuristic v1"]
