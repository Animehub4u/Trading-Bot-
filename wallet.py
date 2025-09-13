import os
from solana.keypair import Keypair
from solana.rpc.api import Client
from dotenv import load_dotenv

load_dotenv()

# Load RPC endpoint (default = mainnet)
RPC_URL = os.getenv("SOLANA_RPC", "https://api.mainnet-beta.solana.com")
client = Client(RPC_URL)

class Wallet:
    def __init__(self):
        private_key = os.getenv("SOL_PRIVATE_KEY")

        if not private_key:
            raise ValueError("❌ SOL_PRIVATE_KEY not set in .env")

        # Convert comma-separated key into bytes
        secret = [int(k) for k in private_key.split(",")]
        self.keypair = Keypair.from_secret_key(bytes(secret))
        self.public_key = str(self.keypair.public_key)

    def get_balance(self):
        balance = client.get_balance(self.keypair.public_key)
        return balance['result']['value'] / 1e9  # SOL

    def send(self, to, amount):
        # TODO: implement send transaction
        print(f"🚀 Would send {amount} SOL to {to} (real tx to be added)")

