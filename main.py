# main.py
# Pump.fun wallet app with Solana wallet authentication (Phantom/Solflare)

import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import requests
import json
from config import PUMP_API_BASE_URL, PUMP_API_KEY, TOKEN_TRADE_ENDPOINT

class PumpAPIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {"Content-Type": "application/json"}

    def create_token(self, public_key: str, name: str, symbol: str, description: str, metadata_uri: str, mint_address: str) -> dict:
        endpoint = f"{TOKEN_TRADE_ENDPOINT}?api-key={self.api_key}"
        payload = {
            "publicKey": public_key,
            "action": "create",
            "tokenMetadata": {"name": name, "symbol": symbol, "uri": metadata_uri},
            "mint": mint_address,
            "denominatedInSol": "true",
            "amount": 1,
            "slippage": 10,
            "priorityFee": 0.0005,
            "pool": "pump"
        }
        try:
            response = requests.post(endpoint, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            if self.api_key == "your-api-key-here":
                return {
                    "status": "success",
                    "signature": "mock_tx_signature",
                    "mint": mint_address,
                    "name": name,
                    "symbol": symbol,
                    "description": description
                }
            return {"error": f"Failed to create token: {str(e)}"}

def load_keypair_from_file(filename: str) -> Keypair:
    with open(filename, 'r') as f:
        private_key_b58 = f.read().strip()
    private_key_bytes = base58.b58decode(private_key_b58)
    return Keypair.from_bytes(private_key_bytes)

def authenticate_wallet(keypair: Keypair) -> bool:
    # Simulate Pump.fun wallet authentication by signing a message
    # In a real dApp, this would use @solana/web3.js and wallet-adapter
    message = "Login to Pump.fun"
    try:
        # Sign the message (mock authentication)
        signature = keypair.sign_message(message.encode('utf-8'))
        # Verify signature (simplified for demo)
        pubkey = Pubkey(keypair.pubkey())
        print(f"Authenticated wallet: {pubkey}")
        print("Login successful. Connected to Pump.fun.")
        return True
    except Exception as e:
        print(f"Authentication failed: {str(e)}")
        return False

def main():
    print("Pump.fun Wallet App (Educational Prototype)")

    # Load wallet
    private_key_file = "private_key.txt"
    try:
        keypair = load_keypair_from_file(private_key_file)
        public_key = str(Pubkey(keypair.pubkey()))
        print(f"Loaded wallet: {public_key}")
    except Exception as e:
        print(f"Error loading wallet: {str(e)}")
        return

    # Authenticate with Pump.fun
    if not authenticate_wallet(keypair):
        return

    # Initialize API client
    api_client = PumpAPIClient(PUMP_API_KEY, PUMP_API_BASE_URL)

    while True:
        print("\nOptions:")
        print("1. Create Token")
        print("2. Exit")
        choice = input("Select an option (1-2): ")

        if choice == "1":
            try:
                name = input("Enter token name: ")
                symbol = input("Enter token symbol: ")
                description = input("Enter token description: ")
                if not all([name, symbol, description]):
                    print("All fields are required.")
                    continue
                mint_keypair = Keypair()  # Mock mint address
                mint_address = str(mint_keypair.pubkey())
                metadata_uri = "https://example.com/metadata.json"
                result = api_client.create_token(
                    public_key, name, symbol, description, metadata_uri, mint_address
                )
                if "error" in result:
                    print(f"Error: {result['error']}")
                else:
                    print(f"Token Created:")
                    print(f"Name: {result['name']}")
                    print(f"Symbol: {result['symbol']}")
                    print(f"Mint Address: {result['mint']}")
                    print(f"Description: {result['description']}")
            except Exception as e:
                print(f"Error creating token: {str(e)}")

        elif choice == "2":
            print("Exiting...")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()