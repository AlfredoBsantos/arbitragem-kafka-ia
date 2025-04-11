import json
import time
from kafka import KafkaProducer
from dotenv import load_dotenv
import os
from utils.web3_utils import get_web3, get_price_data
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))



load_dotenv()

KAFKA_BROKER = os.getenv("KAFKA_BROKER")
producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

while True:
    try:
        price_data_list = get_price_data()
        for data in price_data_list:
            producer.send("dex-prices", data)
            print("Enviado:", data)
    except Exception as e:
        print("Erro:", e)

    time.sleep(10)  # frequência de coleta
