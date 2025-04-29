# token_manager.py
# Manages token creation

from dataclasses import dataclass
from api_client import PumpAPIClient

@dataclass
class Token:
    mint_address: str
    name: str
    symbol: str
    description: str
    metadata_uri: str

class TokenManager:
    def __init__(self, api_client: PumpAPIClient):
        self.api_client = api_client

    def create_token(self, wallet_public_key: str, name: str, symbol: str, description: str, metadata_uri: str, mint_address: str) -> Token:
        """Create a new token."""
        token_data = {
            "name": name,
            "symbol": symbol,
            "description": description,
            "metadata_uri": metadata_uri,
            "mint_address": mint_address
        }
        result = self.api_client.create_token(wallet_public_key, token_data)
        if "error" in result:
            raise Exception(result["error"])
        return Token(
            mint_address=mint_address,
            name=name,
            symbol=symbol,
            description=description,
            metadata_uri=metadata_uri
        )
