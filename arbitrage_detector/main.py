# arbitrage_detector/main.py

import json
from kafka import KafkaConsumer, KafkaProducer
from datetime import datetime

# Dicionário para armazenar o último preço de cada DEX
latest_prices = {}

# Margem mínima para considerar arbitragem (0.5%)
ARBITRAGE_THRESHOLD = 0.005

# Producer Kafka
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def check_arbitrage():
    if len(latest_prices) < 2:
        return

    dex_a, dex_b = list(latest_prices.keys())
    price_a, price_b = latest_prices[dex_a], latest_prices[dex_b]

    price_diff = abs(price_a - price_b)
    percent_diff = price_diff / min(price_a, price_b)

    if percent_diff >= ARBITRAGE_THRESHOLD:
        cheaper_dex = dex_a if price_a < price_b else dex_b
        expensive_dex = dex_b if price_a < price_b else dex_a
        cheaper_price = min(price_a, price_b)
        expensive_price = max(price_a, price_b)
        profit_pct = ((expensive_price - cheaper_price) / cheaper_price) * 100
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Log da oportunidade
        print(f"""
🚨 ARBITRAGEM DETECTADA! {now}
🔄 Comprar em: {cheaper_dex} - Preço: {cheaper_price}
💰 Vender em: {expensive_dex} - Preço: {expensive_price}
📈 Diferença: {price_diff:.6f}
📊 Lucro estimado: {profit_pct:.4f}%
""")

        # Enviar para o tópico Kafka
        arbitrage_data = {
            'buy_dex': cheaper_dex,
            'sell_dex': expensive_dex,
            'buy_price': cheaper_price,
            'sell_price': expensive_price,
            'profit_pct': profit_pct,
            'timestamp': now
        }

        producer.send('arbitrage-opportunities', arbitrage_data)

def main():
    consumer = KafkaConsumer(
        'dex-prices',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='arbitrage-detector'
    )

    print("📡 Detector de Arbitragem Iniciado...\n")
    try:
        for message in consumer:
            data = message.value
            dex = data['dex']
            price = data['price']

            latest_prices[dex] = price
            check_arbitrage()
    except KeyboardInterrupt:
        print("\n🛑 Interrompido pelo usuário.")
    finally:
        consumer.close()
        producer.close()
        print("🔚 Detector finalizado.")

if __name__ == "__main__":
    main()
