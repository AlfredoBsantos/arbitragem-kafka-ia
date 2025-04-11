import json
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

INFURA_URL = os.getenv("INFURA_URL")
web3 = Web3(Web3.HTTPProvider(INFURA_URL))

with open("contracts/UniswapV2Pair.json") as f:
    ABI = json.load(f)

def get_web3():
    return web3

def get_price_data():
    data = []

    # UniswapV2 - ETH/USDC
    uniswap_pair = web3.eth.contract(
        address=Web3.to_checksum_address("0xB4e16d0168e52d35CaCD2c6185b44281Ec28C9Dc"),
        abi=ABI
    )
    reserves = uniswap_pair.functions.getReserves().call()
    price = reserves[0] / reserves[1] / (10 ** (6 - 18))
    data.append({
        "dex": "UniswapV2",
        "pair": "ETH/USDC",
        "price": round(price, 6),
        "block": web3.eth.block_number,
        "timestamp": int(web3.eth.get_block('latest')["timestamp"])
    })

    # Sushiswap - ETH/USDC
    sushiswap_pair = web3.eth.contract(
        address=Web3.to_checksum_address("0x397FF1542f962076d0BFE58eA045FfA2d347ACa0"),
        abi=ABI
    )
    reserves = sushiswap_pair.functions.getReserves().call()
    price = reserves[0] / reserves[1] / (10 ** (6 - 18))
    data.append({
        "dex": "Sushiswap",
        "pair": "ETH/USDC",
        "price": round(price, 6),
        "block": web3.eth.block_number,
        "timestamp": int(web3.eth.get_block('latest')["timestamp"])
    })

    return data
