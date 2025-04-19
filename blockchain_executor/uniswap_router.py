import json
from web3 import Web3
from blockchain_executor.client import w3

# Endereço real do Uniswap V2 Router na mainnet
UNISWAP_ROUTER_ADDRESS = "0x7a250d5630b4cf539739df2c5dacab4b138f9574"

with open("contracts/UniswapV2Router.json") as f:
    abi = json.load(f)["abi"]

router = w3.eth.contract(address=UNISWAP_ROUTER_ADDRESS, abi=abi)

def swap(token_in, token_out, amount_in, amount_out_min, recipient):
    deadline = w3.eth.get_block("latest")["timestamp"] + 300
    path = [token_in, token_out]
    
    tx = router.functions.swapExactTokensForTokens(
        amount_in, amount_out_min, path, recipient, deadline
    ).transact()
    
    return w3.eth.wait_for_transaction_receipt(tx)
