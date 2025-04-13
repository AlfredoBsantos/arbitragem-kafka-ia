# blockchain_executor/uniswap_router.py

from .client import web3, get_account
import json
import os
from web3.exceptions import ContractLogicError

# Caminho para o ABI do UniswapV2Router
ABI_PATH = os.path.join(os.path.dirname(__file__), 'abis', 'uniswap_router_abi.json')

# ⚠️ Atualize com o endereço real do Router na Sepolia (ou seu mock)
ROUTER_ADDRESS = web3.to_checksum_address("0xSEU_ENDERECO_DO_ROUTER")

# Carregar ABI do contrato
with open(ABI_PATH) as f:
    router_abi = json.load(f)

router_contract = web3.eth.contract(address=ROUTER_ADDRESS, abi=router_abi)

def execute_swap(from_token, to_token, amount_in_wei):
    account = get_account()
    address = account["address"]
    private_key = account["private_key"]
    nonce = web3.eth.get_transaction_count(address)

    try:
        print(f"🔧 Preparando swap de {from_token} para {to_token} com {amount_in_wei} wei...")

        # Define rota e deadline
        path = [web3.to_checksum_address(from_token), web3.to_checksum_address(to_token)]
        deadline = web3.eth.get_block("latest")["timestamp"] + 120  # 2 minutos

        # Monta a transação
        tx = router_contract.functions.swapExactTokensForTokens(
            amount_in_wei,     # amountIn
            0,                 # amountOutMin (poderíamos calcular via getAmountsOut)
            path,              # path
            address,           # to
            deadline           # deadline
        ).build_transaction({
            'from': address,
            'gas': 300_000,
            'gasPrice': web3.to_wei('5', 'gwei'),
            'nonce': nonce,
        })

        # Assina e envia
        signed_tx = web3.eth.account.sign_transaction(tx, private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        print(f"🚀 Swap enviado! Tx Hash: {web3.to_hex(tx_hash)}")

    except ContractLogicError as e:
        print(f"❌ Erro no contrato: {e}")
    except Exception as e:
        print(f"⚠️ Erro inesperado ao tentar executar o swap: {e}")
