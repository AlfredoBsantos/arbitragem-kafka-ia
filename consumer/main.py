# consumer/main.py

import json
from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer(
        'dex-prices',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='earliest',  # Pode usar 'earliest' se quiser consumir tudo desde o começo
        enable_auto_commit=True,
        group_id='price-consumer-group'
    )

    print("🟢 Consumidor iniciado. Aguardando mensagens...\n")
    try:
        for message in consumer:
            print(f"🔹 Mensagem recebida: {message.value}")
    except KeyboardInterrupt:
        print("\n⛔ Interrompido pelo usuário.")
    finally:
        consumer.close()
        print("🔚 Consumer finalizado.")


if __name__ == "__main__":
    main()
