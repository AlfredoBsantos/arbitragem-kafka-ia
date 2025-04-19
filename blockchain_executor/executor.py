from web3 import Web3
import json

print("Iniciando a execução da arbitragem...")

# Conectar ao nó local Hardhat
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# ABI gerado após a compilação do contrato Arbitrage
arbitrage_abi = json.loads("""
[
  {
    "inputs": [
      {
        "internalType": "address",
        "name": "_uniswapAddress",
        "type": "address"
      }
    ],
    "stateMutability": "nonpayable",
    "type": "constructor"
  },
  {
    "inputs": [],
    "name": "getRateFromUniswap",
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "owner",
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  },
  {
    "inputs": [],
    "name": "uniswap",
    "outputs": [
      {
        "internalType": "contract IUniswapMock",
        "name": "",
        "type": "address"
      }
    ],
    "stateMutability": "view",
    "type": "function"
  }
]
""")

# Substitua com o endereço real do contrato Arbitrage (copie do terminal ao rodar deploy.js)
arbitrage_address = "COLE_O_ENDERECO_DO_CONTRATO_AQUI"

# Instanciar o contrato
arbitrage_contract = w3.eth.contract(address=arbitrage_address, abi=arbitrage_abi)

def get_uniswap_rate():
    return arbitrage_contract.functions.getRateFromUniswap().call()

def execute_arbitrage():
    uniswap_rate = get_uniswap_rate()
    print("Taxa obtida do UniswapMock:", uniswap_rate)

# Rodar
execute_arbitrage()
print("Execução da arbitragem concluída.")
# A execução da arbitragem foi concluída com sucesso. Você pode verificar o resultado no console. 