# main.py
# Main app with PyQt5 GUI

import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton,
                             QTextEdit, QLineEdit, QLabel, QFormLayout, QMessageBox)
from wallet_manager import WalletManager, Wallet
from token_manager import TokenManager
from api_client import PumpAPIClient
from config import SOLANA_RPC, PUMP_API_BASE_URL, PUMP_API_KEY
from solders.keypair import Keypair

class PumpFunApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pump.fun Wallet App (Educational)")
        self.setGeometry(100, 100, 600, 400)

        # Initialize managers
        self.wallet_manager = WalletManager(SOLANA_RPC)
        self.api_client = PumpAPIClient(PUMP_API_KEY, PUMP_API_BASE_URL)
        self.token_manager = TokenManager(self.api_client)

        # Set up UI
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Wallet section
        self.create_wallet_btn = QPushButton("Create Wallet")
        self.create_wallet_btn.clicked.connect(self.create_wallet)
        self.layout.addWidget(self.create_wallet_btn)

        self.wallet_output = QTextEdit()
        self.wallet_output.setReadOnly(True)
        self.layout.addWidget(QLabel("Wallet Details:"))
        self.layout.addWidget(self.wallet_output)

        # Token creation form
        self.token_form = QWidget()
        self.token_layout = QFormLayout(self.token_form)
        self.public_key_input = QLineEdit()
        self.name_input = QLineEdit()
        self.symbol_input = QLineEdit()
        self.description_input = QLineEdit()
        self.token_layout.addRow("Wallet Public Key:", self.public_key_input)
        self.token_layout.addRow("Token Name:", self.name_input)
        self.token_layout.addRow("Token Symbol:", self.symbol_input)
        self.token_layout.addRow("Token Description:", self.description_input)
        self.create_token_btn = QPushButton("Create Token")
        self.create_token_btn.clicked.connect(self.create_token)
        self.token_layout.addWidget(self.create_token_btn)
        self.layout.addWidget(QLabel("Create Token:"))
        self.layout.addWidget(self.token_form)

        # Token output
        self.token_output = QTextEdit()
        self.token_output.setReadOnly(True)
        self.layout.addWidget(QLabel("Token Creation Result:"))
        self.layout.addWidget(self.token_output)

    def create_wallet(self):
        """Create a new wallet and display details."""
        try:
            wallet = self.wallet_manager.create_wallet()
            filename = f"wallet_{wallet.public_key[:8]}.txt"
            self.wallet_manager.save_wallet(wallet, filename)
            output = (f"Wallet Created:\n"
                      f"Public Key: {wallet.public_key}\n"
                      f"Private Key: {wallet.private_key}\n"
                      f"Balance: {wallet.balance} SOL\n"
                      f"Token Accounts:\n")
            for token in wallet.tokens:
                output += f"  Mint: {token['mint']}, Amount: {token['amount']}, Address: {token['address']}\n"
            output += f"\nSaved to: {filename}\n"
            output += "To use with Pump.fun:\n1. Import private key into Phantom/Solflare.\n2. Connect wallet on Pump.fun website."
            self.wallet_output.setText(output)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create wallet: {str(e)}")

    def create_token(self):
        """Simulate creating a token."""
        try:
            public_key = self.public_key_input.text()
            name = self.name_input.text()
            symbol = self.symbol_input.text()
            description = self.description_input.text()
            if not all([public_key, name, symbol, description]):
                raise ValueError("All fields are required.")
            # Generate mock mint address
            mint_keypair = Keypair()
            mint_address = str(mint_keypair.pubkey())
            metadata_uri = "https://example.com/metadata.json"  # Mock URI
            token = self.token_manager.create_token(
                public_key, name, symbol, description, metadata_uri, mint_address
            )
            self.token_output.setText(
                f"Token Created:\n"
                f"Name: {token.name}\n"
                f"Symbol: {token.symbol}\n"
                f"Mint Address: {token.mint_address}\n"
                f"Description: {token.description}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to create token: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PumpFunApp()
    window.show()
    sys.exit(app.exec_())
