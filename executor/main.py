# executor/main.py

import json
from kafka import KafkaConsumer

def main():
    consumer = KafkaConsumer(
        'arbitrage-opportunities',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda m: json.loads(m.decode('utf-8')),
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='arbitrage-executor'
    )

    print("⚙️  Executor de Arbitragem Iniciado...\n")

    try:
        for message in consumer:
            data = message.value
            print(f"""
✅ Executando Arbitragem:
🔄 Comprar em: {data['buy_dex']} - Preço: {data['buy_price']}
💰 Vender em: {data['sell_dex']} - Preço: {data['sell_price']}
📊 Lucro estimado: {data['profit_pct']:.2f}%
⏰ Horário: {data['timestamp']}
            """)
    except KeyboardInterrupt:
        print("\n🛑 Executor interrompido pelo usuário.")
    finally:
        consumer.close()
        print("🔚 Executor finalizado.")

if __name__ == "__main__":
    main()
