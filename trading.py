import logging

def auto_trade(token, amount_sol=0.1, take_profit=50, stop_loss=20):
    """
    Simulated trading logic.
    (Later: integrate with Solana wallet SDK or Jupiter aggregator)
    """
    msg = (
        f"📈 Auto-Buy {amount_sol} SOL of {token['symbol']} ({token['address']})\n"
        f"🎯 TP: +{take_profit}% | 🛑 SL: -{stop_loss}%"
    )
    print(msg)
    logging.info(f"Trade executed: {msg}")
