from web3 import Web3

# RPC do fork do Hardhat
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Conta Hardhat fictícia (tem saldo alto por padrão)
DEFAULT_ACCOUNT = w3.eth.accounts[0]
w3.eth.default_account = DEFAULT_ACCOUNT

print("Conectado:", w3.is_connected())
