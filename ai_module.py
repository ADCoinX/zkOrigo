# ai_module.py - Heuristic AI v2 (7 chains)

def score_wallet(chain: str, address: str, chain_result: dict):
    reasons = []
    score = 50  # baseline neutral

    # Rule 1: endpoint fail
    if chain_result.get("error"):
        score += 20
        reasons.append("Chain endpoint fallback triggered")

    # Rule 2: address entropy rendah
    addr = address.lower().replace("0x","")
    if len(set(addr)) < len(addr)/4:
        score += 15
        reasons.append("Low entropy in address")

    # Rule 3: address terlalu pendek
    if len(addr) < 20:
        score += 10
        reasons.append("Short address length")

    # Rule 4: dormant wallet (tiada balance)
    if chain_result.get("balance") in (None, "0", 0):
        score += 10
        reasons.append("Dormant / empty wallet")

    # Rule 5: chain-specific (7 chains)
    if chain in ("eth", "bnb", "polygon"):
        score += 5
        reasons.append("EVM chain risk +5")
    elif chain == "solana":
        score += 3
        reasons.append("Solana chain risk +3")
    elif chain == "xrpl":
        score -= 3
        reasons.append("XRPL chain stability -3")
    elif chain == "hedera":
        score -= 5
        reasons.append("Enterprise Hedera -5")
    elif chain == "xlm":
        score -= 5
        reasons.append("Enterprise Stellar -5")

    # Clamp supaya 0–100
    score = max(0, min(100, score))

    if not reasons:
        reasons = ["No issues detected"]

    return {
        "risk_score": score,
        "reasons": reasons,
        "version": "heuristic-v2"
    }
