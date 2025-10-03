import httpx

FALLBACK_ENDPOINTS = {
    "eth": [
        "https://rpc.ankr.com/eth",
        "https://cloudflare-eth.com",
        "https://ethereum.publicnode.com"
    ],
    "polygon": [
        "https://polygon-rpc.com",
        "https://rpc-mainnet.matic.quiknode.pro",
        "https://polygon.llamarpc.com"
    ],
    "bnb": [
        "https://bsc-dataseed.binance.org",
        "https://bsc-dataseed1.defibit.io",
        "https://bsc-dataseed1.ninicoin.io"
    ],
    "solana": [
        "https://api.mainnet-beta.solana.com",
        "https://rpc.ankr.com/solana",
        "https://solana.public-rpc.com"
    ],
    "xrpl": [
        "https://s1.ripple.com:51234",
        "https://xrplcluster.com",
        "https://xrpl.ws"
    ],
    "hedera": [
        "https://mainnet-public.mirrornode.hedera.com/api/v1",
        "https://testnet.mirrornode.hedera.com/api/v1",
        "https://backup.hedera.mirrornode/api/v1"
    ],
    "xlm": [
        "https://horizon.stellar.org",
        "https://horizon.stellar.lobstr.co",
        "https://horizon.stellar.expert"
    ]
}


async def check_wallet(chain: str, address: str):
    endpoints = FALLBACK_ENDPOINTS.get(chain, [])
    for url in endpoints:
        try:
            async with httpx.AsyncClient(timeout=10) as client:

                # ----------------
                # EVM Chains (ETH, BNB, Polygon)
                # ----------------
                if chain in ("eth", "polygon", "bnb"):
                    payload = {
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [address, "latest"],
                        "id": 1
                    }
                    r = await client.post(url, json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        wei_balance = int(data["result"], 16)
                        # convert wei -> native coin
                        balance = wei_balance / 10**18
                        return {"balance": balance, "raw": data}

                # ----------------
                # Solana (lamports → SOL)
                # ----------------
                elif chain == "solana":
                    r = await client.post(url, json={
                        "jsonrpc": "2.0",
                        "id": 1,
                        "method": "getBalance",
                        "params": [address]
                    })
                    if r.status_code == 200:
                        data = r.json()
                        lamports = data.get("result", {}).get("value")
                        balance = lamports / 10**9 if lamports else 0  # lamports → SOL
                        return {"balance": balance, "raw": data}

                # ----------------
                # XRPL (drops → XRP)
                # ----------------
                elif chain == "xrpl":
                    r = await client.post(url, json={
                        "method": "account_info",
                        "params": [{"account": address}]
                    })
                    if r.status_code == 200:
                        data = r.json()
                        drops = data.get("result", {}).get("account_data", {}).get("Balance")
                        balance = int(drops) / 10**6 if drops else 0  # drops → XRP
                        return {"balance": balance, "raw": data}

                # ----------------
                # Hedera (tinybars → HBAR)
                # ----------------
                elif chain == "hedera":
                    r = await client.get(f"{url}/accounts/{address}")
                    if r.status_code == 200:
                        data = r.json()
                        tinybars = None
                        if "balance" in data and isinstance(data["balance"], dict):
                            tinybars = data["balance"].get("balance")
                        balance = int(tinybars) / 10**8 if tinybars else 0  # tinybars → HBAR
                        return {"balance": balance, "raw": data}

                # ----------------
                # Stellar (direct balances → XLM)
                # ----------------
                elif chain == "xlm":
                    r = await client.get(f"{url}/accounts/{address}")
                    if r.status_code == 200:
                        data = r.json()
                        balances = data.get("balances", [])
                        native_balance = None
                        for b in balances:
                            if b.get("asset_type") == "native":  # lumens
                                native_balance = b.get("balance")
                        return {"balance": float(native_balance) if native_balance else 0, "raw": data}

        except Exception:
            continue

    return {"error": f"All endpoints failed for {chain}"}
