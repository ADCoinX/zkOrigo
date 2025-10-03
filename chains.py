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
        "wss://xrpl.ws"
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
                if chain == "eth":
                    payload = {
                        "jsonrpc": "2.0",
                        "method": "eth_getBalance",
                        "params": [address, "latest"],
                        "id": 1
                    }
                    r = await client.post(url, json=payload)
                    if r.status_code == 200:
                        return r.json()
                # TODO: Extend per chain
        except Exception:
            continue
    return {"error": f"All endpoints failed for {chain}"}
