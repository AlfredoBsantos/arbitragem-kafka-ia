from blockchain_executor.flashloan_executor import execute_flashloan
from blockchain_executor.swap_executor import perform_arbitrage
from web3 import Web3

# Simulação com WETH e USDC na mainnet
WETH = "0xC02aaa39b223FE8D0A0e5C4F27eAD9083C756Cc2"
USDC = "0xA0b86991C6218B36c1D19D4a2e9Eb0cE3606EB48"

if __name__ == "__main__":
    print("Iniciando Arbitragem com Flashloan")
    
    # Step 1: pega emprestado via flashloan (em WETH por exemplo)
    receipt = execute_flashloan(WETH, Web3.to_wei(10, "ether"))
    
    print("Flashloan executado:", receipt.transactionHash.hex())

    # Step 2: arbitragem (pode acontecer dentro do contrato ou aqui)
    perform_arbitrage(WETH, USDC, Web3.to_wei(10, "ether"))
