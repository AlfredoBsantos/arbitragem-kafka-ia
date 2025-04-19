from web3 import Web3
from blockchain_executor.client import w3
import json

# Carrega ABI e endereço do contrato de execução
with open("contracts/ArbitrageExecutor.json") as f:
    abi = json.load(f)["abi"]

# Endereço mock do contrato já deployado
ARBITRAGE_EXECUTOR_ADDRESS = "0xYourDeployedContractAddress"

contract = w3.eth.contract(address=ARBITRAGE_EXECUTOR_ADDRESS, abi=abi)

def execute_flashloan(token, amount):
    tx = contract.functions.executeFlashloan(token, amount).transact()
    receipt = w3.eth.wait_for_transaction_receipt(tx)
    return receipt
