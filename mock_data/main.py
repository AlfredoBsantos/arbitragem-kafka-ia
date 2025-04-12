# mock_data/main.py

import json
import time
from kafka import KafkaProducer
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = 'dex-prices'

def main():
    block = 22247799
    while True:
        timestamp = int(time.time())

        # Preços fixos com diferença forçada de 5%
        uniswap_price = 100.00
        sushiswap_price = 105.00

        uniswap_data = {
            'dex': 'UniswapV2',
            'pair': 'ETH/USDC',
            'price': uniswap_price,
            'block': block,
            'timestamp': timestamp
        }

        sushiswap_data = {
            'dex': 'Sushiswap',
            'pair': 'ETH/USDC',
            'price': sushiswap_price,
            'block': block,
            'timestamp': timestamp
        }

        producer.send(TOPIC, value=uniswap_data)
        print(f"Enviado: {uniswap_data}")

        producer.send(TOPIC, value=sushiswap_data)
        print(f"Enviado: {sushiswap_data}")

        block += 1
        time.sleep(5)  # Envia a cada 5 segundos

if __name__ == "__main__":
    main()
