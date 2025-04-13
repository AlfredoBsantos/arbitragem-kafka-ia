# blockchain_executor/client.py

from web3 import Web3
from dotenv import load_dotenv
import os

load_dotenv()

RPC_URL = os.getenv("RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
PUBLIC_ADDRESS = os.getenv("PUBLIC_ADDRESS")

web3 = Web3(Web3.HTTPProvider(RPC_URL))

def get_account():
    return {
        "address": PUBLIC_ADDRESS,
        "private_key": PRIVATE_KEY
    }

def is_connected():
    return web3.is_connected()
