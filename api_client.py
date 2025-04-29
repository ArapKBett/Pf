# api_client.py
# Simulates Pump.fun API interactions

import requests
import json
from config import PUMP_API_BASE_URL, PUMP_API_KEY, MOCK_TOKEN_ENDPOINT

class PumpAPIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def create_token(self, wallet_public_key: str, token_data: dict) -> dict:
        """Simulate creating a token (based on PumpPortal API structure)."""
        payload = {
            "publicKey": wallet_public_key,
            "action": "create",
            "tokenMetadata": {
                "name": token_data["name"],
                "symbol": token_data["symbol"],
                "uri": token_data["metadata_uri"]
            },
            "mint": token_data["mint_address"],
            "denominatedInSol": "true",
            "amount": 1,  # 1 SOL for dev buy
            "slippage": 10,
            "priorityFee": 0.0005,
            "pool": "pump"
        }
        try:
            response = requests.post(
                MOCK_TOKEN_ENDPOINT,
                headers=self.headers,
                data=json.dumps(payload)
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": f"Failed to create token: {str(e)}"}
