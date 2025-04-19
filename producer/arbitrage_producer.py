import json
import random
import time
from kafka import KafkaProducer

# Configurações
KAFKA_BROKER = 'localhost:9092'
TOPIC = 'arbitrage-prices'

# Inicializa o producer Kafka
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("[Producer] Iniciando envio de preços de arbitragem...")

try:
    while True:
        # Gera dados simulados
        token_in = "0xTokenA"
        token_out = "0xTokenB"
        rate = random.uniform(0.8, 1.2)  # Ex: taxa de câmbio simulada

        data = {
            "token_in": token_in,
            "token_out": token_out,
            "rate": round(rate, 6)
        }

        print(f"[Producer] Enviando: {data}")
        producer.send(TOPIC, value=data)

        time.sleep(3)

except KeyboardInterrupt:
    print("\n[Producer] Encerrado manualmente.")
finally:
    producer.close()
