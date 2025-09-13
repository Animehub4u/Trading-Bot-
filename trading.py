import requests
import os
import logging

JUP_API = "https://quote-api.jup.ag/v6"

def get_quote(input_mint, output_mint, amount):
    """Get best swap route from Jupiter"""
    url = f"{JUP_API}/quote?inputMint={input_mint}&outputMint={output_mint}&amount={amount}&slippageBps=50"
    res = requests.get(url)
    res.raise_for_status()
    return res.json()

def auto_trade(token, amount_sol=0.1, take_profit=50, stop_loss=20):
    """
    Execute trade via Jupiter API
    (Right now: fetches route, later: submit signed tx)
    """
    # SOL mint & token mint
    SOL_MINT = "So11111111111111111111111111111111111111112"
    token_mint = token['address']

    lamports = int(amount_sol * 1e9)

    try:
        quote = get_quote(SOL_MINT, token_mint, lamports)
        best_route = quote['data'][0]

        msg = (
            f"📈 Buy {amount_sol} SOL of {token['symbol']} ({token_mint})\n"
            f"Route: {best_route['marketInfos'][0]['label']}\n"
            f"🎯 TP: {take_profit}% | 🛑 SL: {stop_loss}%"
        )
        print(msg)
        logging.info(f"Trade planned: {msg}")

        # 🔹 Next step: Build & send transaction via Jupiter swap API
        # POST /swap (need wallet signing)

    except Exception as e:
        logging.error(f"Trade failed: {e}")
        print(f"❌ Trade error: {e}")
