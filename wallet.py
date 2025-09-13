class Wallet:
    def __init__(self):
        # In real setup, load private key securely
        self.public_key = "FakeWallet12345"
        self.balance_sol = 10.0

    def get_balance(self):
        return self.balance_sol

    def send(self, to, amount):
        if amount > self.balance_sol:
            print("❌ Not enough SOL")
        else:
            self.balance_sol -= amount
            print(f"✅ Sent {amount} SOL to {to}. New balance: {self.balance_sol} SOL")
