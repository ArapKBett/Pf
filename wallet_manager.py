# wallet_manager.py
# Handles Solana wallet creation and RPC queries

from solders.keypair import Keypair
from solana.rpc.api import Client
from solana.rpc.types import TokenAccountOpts
import base58
from dataclasses import dataclass

@dataclass
class Wallet:
    public_key: str
    private_key: str
    balance: float
    tokens: list

class WalletManager:
    def __init__(self, rpc_endpoint: str):
        self.rpc_endpoint = rpc_endpoint
        self.client = Client(rpc_endpoint)

    def create_wallet(self) -> Wallet:
        """Create a new Solana wallet."""
        keypair = Keypair()
        public_key = str(keypair.pubkey())
        private_key = base58.b58encode(keypair.to_bytes()).decode('utf-8')
        balance = self.get_balance(public_key)
        tokens = self.get_token_accounts(public_key)
        return Wallet(public_key=public_key, private_key=private_key, balance=balance, tokens=tokens)

    def get_balance(self, public_key: str) -> float:
        """Query Solana RPC for wallet balance."""
        try:
            balance = self.client.get_balance(pubkey=public_key).value
            return balance / 1_000_000_000  # Convert lamports to SOL
        except Exception as e:
            print(f"Error querying balance: {e}")
            return 0.0

    def get_token_accounts(self, public_key: str) -> list:
        """Query Solana RPC for SPL token accounts."""
        try:
            response = self.client.get_token_accounts_by_owner(
                pubkey=public_key,
                opts=TokenAccountOpts(program_id="TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"),
                encoding="jsonParsed"
            )
            tokens = []
            for account in response.value:
                info = account.account.data.parsed["info"]
                tokens.append({
                    "mint": info["mint"],
                    "amount": info["tokenAmount"]["uiAmount"],
                    "address": str(account.pubkey)
                })
            return tokens
        except Exception as e:
            print(f"Error querying token accounts: {e}")
            return []

    def save_wallet(self, wallet: Wallet, filename: str):
        """Save wallet details to a file for manual import."""
        with open(filename, 'w') as f:
            f.write(f"Public Key: {wallet.public_key}\n")
            f.write(f"Private Key: {wallet.private_key}\n")
            f.write(f"Balance: {wallet.balance} SOL\n")
            f.write("Token Accounts:\n")
            for token in wallet.tokens:
                f.write(f"  Mint: {token['mint']}, Amount: {token['amount']}, Address: {token['address']}\n")
