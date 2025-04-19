# 🚀 Crypto Arbitrage System

Um projeto completo de **arbitragem de criptomoedas** utilizando **Flash Loans**, **Smart Contracts (Solidity)**, **Python**, e **Apache Kafka**. O sistema é modular, altamente escalável, e pode ser utilizado como base para estratégias de arbitragem entre exchanges descentralizadas (DEXs).

---

## 🧠 Visão Geral

Este projeto automatiza a identificação e execução de oportunidades de arbitragem entre diferentes plataformas DeFi. Ele foi projetado para simular a arbitragem com contratos inteligentes e integrações reais, permitindo testes e desenvolvimento seguro antes da execução em produção.

---

## 🧩 Estrutura do Projeto
```bash
crypto-arbitrage-project/ │ ├── blockchain_executor/ # Executa arbitragem via contrato inteligente │ └── executor.py │ ├── consumer/ # Consumidor Kafka: escuta e processa dados de preços │ └── price_consumer.py │ ├── contracts/ # Contratos inteligentes (Solidity) │ └── Arbitrage.sol │ ├── hardhat-env/ # Projeto Hardhat para testes de contrato │ └── scripts/ │ └── test/ │ └── hardhat.config.js │ ├── producer/ # Produtor Kafka: envia dados de preço │ └── price_producer.py │ ├── utils/ # Funções auxiliares │ ├── run_all.sh # Script para executar todos os serviços │ ├── .gitignore └── README.md
```

---

## ⚙️ Tecnologias Utilizadas

- **Solidity** (Smart Contracts)
- **Hardhat** (Ambiente de desenvolvimento Ethereum)
- **Python 3.10+**
- **Apache Kafka** (Mensageria entre módulos)
- **Web3.py**
- **Ganache / Hardhat Node** (Blockchain local para testes)
- **Shell Script** (`run_all.sh` para automação)

---

## 🚀 Como Executar

### Pré-requisitos:

- Python 3.10+
- Node.js + npm
- Hardhat CLI
- Ganache ou Hardhat local node
- Kafka + Zookeeper

### Instalação:

```bash
# Instalar dependências Python
pip install -r requirements.txt

# Instalar dependências do Hardhat
cd hardhat-env
npm install

#Execultar tudo
chmod +x run_all.sh
./run_all.sh
```

📈 Funcionalidades
✅ Publica e consome preços via Kafka

✅ Contrato inteligente de arbitragem (Mock Uniswap incluído)

✅ Integração com Web3 via Python

✅ Execução automática de arbitragem via executor.py

✅ Script de automação para execução completa


### 📂 O que ainda falta?

 
 Adicionar suporte a múltiplas DEXs (SushiSwap, Aave, etc)

 Implementar Flash Loans reais (Aave)

 Conectar com uma rede de teste (Goerli, Sepolia)

 Interface Web para monitoramento (futuramente)

🧑‍💻 Autor
Desenvolvido por Alfredo Henrique Silveira Bezerra dos Santos – Estudante de ADS @ UFRN-EAJ
Orientação: xxx

🛡️ Aviso Legal
Este projeto é para fins educacionais e de pesquisa. O uso em ambientes reais de produção ou com fundos reais deve ser feito com extrema cautela. Nenhuma responsabilidade será assumida por perdas ou danos.

⭐ Gostou?
Deixe uma ⭐ se curtir o projeto ou quiser contribuir!






