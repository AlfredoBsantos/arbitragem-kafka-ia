# 📊 Arbitragem entre DEXs com Kafka e Python

Este projeto tem como objetivo detectar e simular oportunidades de **arbitragem de criptomoedas** entre diferentes DEXs (como Uniswap e Sushiswap), utilizando **Kafka** como sistema de mensageria e comunicação entre módulos.

---

## 🚀 Visão Geral

O sistema é composto por três módulos principais:

- **mock_data**: simula preços de ativos em diferentes DEXs e envia para Kafka.
- **arbitrage_detector**: consome os dados e detecta oportunidades de arbitragem.
- **executor**: escuta eventos de arbitragem detectada e executa a simulação da compra/venda.

---

## 📁 Estrutura do Projeto

```
arbitragem-kafka-ia/
│
├── mock_data/
│   └── main.py          ← Simula dados de preços
│
├── arbitrage_detector/
│   └── main.py          ← Detecta arbitragem e publica evento
│
├── executor/
│   └── main.py          ← Executa arbitragem ao detectar evento
│
├── requirements.txt     ← Dependências do projeto
└── README.md            ← Este arquivo
```

---

## 🔧 Requisitos

- Python 3.10+
- Apache Kafka e Zookeeper instalados localmente

Instale os pacotes do projeto:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Como Rodar

1. Inicie o Kafka e o Zookeeper:
```bash
# No diretório do Kafka
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

2. Execute os módulos em terminais separados:

### 1. Mock dos dados:
```bash
python -m mock_data.main
```

### 2. Detector de Arbitragem:
```bash
python -m arbitrage_detector.main
```

### 3. Executor:
```bash
python -m executor.main
```

---

## ✅ O que já está funcionando

- [x] Kafka operando entre os módulos
- [x] Simulação de preços e envio ao Kafka
- [x] Detecção de arbitragem com base em diferença de preços
- [x] Publicação de eventos de arbitragem detectada
- [x] Execução simulada da arbitragem

---

## ⏳ Próximos Passos

- [ ] Salvar logs de arbitragem em arquivos ou banco de dados
- [ ] Medir tempo entre detecção e execução (delay)
- [ ] Adicionar verificação de slippage e liquidez
- [ ] Conectar com Web3 real (RPC/Infura)
- [ ] Execução real via smart contracts (swap simulados)
- [ ] Criar dashboard (web) com histórico de oportunidades
- [ ] Dockerizar os serviços

---

## 🧠 Conceitos Envolvidos

- Arbitragem de criptomoedas
- Microserviços com Kafka
- Simulação de negociação
- Comunicação assíncrona
- Publicação e consumo de mensagens

---

## 🧑‍💻 Autor

**Alfredo**  
Desenvolvedor fullstack e entusiasta de sistemas distribuídos com IA, automações e cripto.