import os
import sys
import requests
import logging
from openai import OpenAI
from dotenv import load_dotenv
from trading import auto_trade
from wallet import Wallet

# Setup logging
os.makedirs("reports", exist_ok=True)
logging.basicConfig(
    filename="reports/bot.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load API keys from .env
load_dotenv()
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# 🔹 Fail safely if key is missing or invalid
if not OPENAI_KEY or not OPENAI_KEY.startswith("sk-"):
    msg = "❌ ERROR: OpenAI API key missing or invalid. Please set it in .env"
    print(msg)
    logging.error(msg)
    sys.exit(1)

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_KEY)


# 🔹 Get trending Solana tokens
def get_trending_tokens():
    try:
        url = "https://api.dexscreener.com/latest/dex/tokens/solana"
        res = requests.get(url, timeout=10)
        res.raise_for_status()
        return res.json().get("pairs", [])
    except Exception as e:
        logging.error(f"Failed to fetch tokens: {e}")
        return []


# 🔹 Filter hidden gems
def filter_hidden_gems(tokens):
    gems = []
    for t in tokens:
        liq = float(t.get("liquidity", {}).get("usd", 0))
        vol = float(t.get("volume", {}).get("h24", 0))
        price_change = float(t.get("priceChange", {}).get("h24", 0))

        # Criteria: small-mid liquidity, big volume, high price move
        if 5000 < liq < 500000 and vol > 20000 and abs(price_change) > 50:
            gems.append({
                "name": t.get("baseToken", {}).get("name"),
                "symbol": t.get("baseToken", {}).get("symbol"),
                "address": t.get("baseToken", {}).get("address"),
                "liq": liq,
                "vol": vol,
                "change24h": price_change
            })
    return gems


# 🔹 AI analysis
def analyze_with_ai(gems, social_data):
    prompt = f"""
You are an expert Solana meme coin analyst. 
Tokens: {gems}  
Social Data: {social_data}  

1. Score each token (0-100).  
2. Explain risks and pump potential.  
3. Recommend: Buy / Hold / Avoid.
    """
    try:
        res = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
        )
        return res.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"OpenAI request failed: {e}")
        return "⚠️ AI analysis unavailable."


# 🔹 Main runner
def run_bot():
    print("🔎 Scanning Solana tokens for hidden gems...")
    tokens = get_trending_tokens()
    gems = filter_hidden_gems(tokens)

    if not gems:
        print("⚪ No hidden gems found.")
        logging.info("No gems found this run.")
        return

    # Fake social mentions (replace with real APIs later)
    social_data = {gem["symbol"]: {"twitter": 200, "reddit": 50, "sentiment": "positive"} for gem in gems}

    ai_report = analyze_with_ai(gems, social_data)
    print("\n🚀 Hidden Gem Report:\n", ai_report)

    # Save AI report
    with open("reports/hidden_gem_report.txt", "w") as f:
        f.write(ai_report)
    logging.info("AI Report saved.")

    # Auto-trading
    for gem in gems:
        logging.info(f"Evaluating trade for {gem['symbol']}")
        if gem["liq"] > 10000 and gem["vol"] > 30000:
            auto_trade(gem, amount_sol=0.1)


if __name__ == "__main__":
    wallet = Wallet()
    print(f"🔑 Wallet: {wallet.public_key} | Balance: {wallet.get_balance()} SOL")
    run_bot()
