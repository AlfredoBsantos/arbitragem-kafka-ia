import json
from kafka import KafkaConsumer
from web3 import Web3
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

ARBITRAGE_ADDRESS = os.getenv("ARBITRAGE_CONTRACT")
ARBITRAGE_ABI_PATH = os.getenv("ARBITRAGE_ABI_PATH")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
ACCOUNT_ADDRESS = os.getenv("PUBLIC_ADDRESS")

# Conexão com Hardhat local
web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
assert web3.is_connected(), "Erro: Web3 não conectado ao Hardhat"

# Carrega apenas a ABI do JSON
with open(ARBITRAGE_ABI_PATH, 'r') as f:
    contract_json = json.load(f)
    abi = contract_json["abi"]  # Certifique-se de que o campo seja exatamente esse

# Instancia contrato
contract = web3.eth.contract(address=ARBITRAGE_ADDRESS, abi=abi)

# Consumer Kafka
consumer = KafkaConsumer(
    'arbitrage-prices',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

print("[Consumer] Escutando arbitrage-prices...")

for msg in consumer:
    data = msg.value
    print(f"[Consumer] Mensagem recebida: {data}")

    # Envia transação pro contrato
    try:
        nonce = web3.eth.get_transaction_count(ACCOUNT_ADDRESS)
        tx = contract.functions.getRateFromUniswap().build_transaction({
            'from': ACCOUNT_ADDRESS,
            'nonce': nonce,
            'gas': 2000000,
            'gasPrice': web3.to_wei('50', 'gwei')
        })

        signed_tx = web3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"[Consumer] Transação enviada! Hash: {tx_hash.hex()}")

    except Exception as e:
        print(f"[Consumer] Erro ao enviar transação: {e}")
