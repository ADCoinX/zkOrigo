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
        "https://xrplcluster.com"
    ],
    "hedera": [
        "https://mainnet-public.mirrornode.hedera.com/api/v1"
    ],
    "xlm": [
        "https://horizon.stellar.org"
    ]
}

async def check_wallet(chain: str, address: str):
    endpoints = FALLBACK_ENDPOINTS.get(chain, [])
    for url in endpoints:
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                if chain in ("eth","polygon","bnb"):
                    # EVM chains -> eth_getBalance
                    payload = {
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [address, "latest"],
                        "id": 1
                    }
                    r = await client.post(url, json=payload)
                    if r.status_code == 200:
                        data = r.json()
                        return {"balance": int(data["result"],16), "raw": data}

                elif chain == "solana":
                    r = await client.post(url, json={"jsonrpc":"2.0","id":1,"method":"getBalance","params":[address]})
                    if r.status_code == 200:
                        data = r.json()
                        return {"balance": data.get("result",{}).get("value"), "raw": data}

                elif chain == "xrpl":
                    r = await client.post(url, json={"method":"account_info","params":[{"account": address}]})
                    if r.status_code == 200:
                        data = r.json()
                        bal = data.get("result",{}).get("account_data",{}).get("Balance")
                        return {"balance": bal, "raw": data}

                elif chain == "hedera":
                    r = await client.get(f"{url}/accounts/{address}")
                    if r.status_code == 200:
                        data = r.json()
                        return {"balance": data.get("balance",{}).get("balance"), "raw": data}

                elif chain == "xlm":
                    r = await client.get(f"{url}/accounts/{address}")
                    if r.status_code == 200:
                        data = r.json()
                        return {"balance": data.get("balances",[]), "raw": data}

        except Exception:
            continue
    return {"error": f"All endpoints failed for {chain}"}
