# config.py
# Configuration settings for the Solana wallet app

# Solana RPC endpoint (devnet for educational purposes)
SOLANA_RPC = "https://api.devnet.solana.com"

# Placeholder Pump.fun API endpoint (use PumpPortal or Bitquery if available)
PUMP_API_BASE_URL = "https://pumpportal.fun/api"
PUMP_API_KEY = "your-api-key-here"  # Replace with real key if using PumpPortal

# Mock endpoints for simulation
MOCK_TOKEN_ENDPOINT = f"{PUMP_API_BASE_URL}/trade"
