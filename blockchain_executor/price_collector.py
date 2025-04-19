import json
import time
import logging
from web3 import Web3
from kafka import KafkaProducer
from kafka.errors import KafkaError
from dotenv import load_dotenv
import os

# Configuração básica de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

class PriceCollector:
    def __init__(self):
        # Configurações do Kafka
        self.kafka_config = {
            'bootstrap_servers': os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092').split(','),
            'value_serializer': lambda v: json.dumps(v).encode('utf-8'),
            'api_version': (3, 4, 0),
            'retries': 5,
            'acks': 'all'
        }
        
        # Conexão com a blockchain
        self.w3 = Web3(Web3.HTTPProvider(
            os.getenv('BLOCKCHAIN_RPC_URL', 'http://localhost:8545')
        ))
        
        if not self.w3.is_connected():
            logger.error("Falha na conexão com a blockchain")
            raise ConnectionError("Não foi possível conectar à blockchain")

        # Configuração dos contratos
        self.uniswap_router = self.w3.eth.contract(
            address=os.getenv('UNISWAP_ROUTER_ADDRESS'),
            abi=self._load_abi('contracts/UniswapV2Router.json')
        )
        
        # Inicializa o producer Kafka
        self.producer = self._init_kafka_producer()
        
        logger.info("PriceCollector inicializado com sucesso")

    def _load_abi(self, file_path):
    
        try:
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            abs_path = os.path.join(project_root, file_path)
            with open(abs_path) as f:
                return json.load(f)['abi']
        except Exception as e:
            logger.er

def _get_fallback_abi(self):
    """Retorna um ABI mínimo essencial para testes"""
    return [
        {
            "inputs": [
                {"internalType": "uint256", "name": "amountIn", "type": "uint256"},
                {"internalType": "address[]", "name": "path", "type": "address[]"}
            ],
            "name": "getAmountsOut",
            "outputs": [
                {"internalType": "uint256[]", "name": "amounts", "type": "uint256[]"}
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]

    def _init_kafka_producer(self):
        """Inicializa e testa a conexão com o Kafka"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                producer = KafkaProducer(**self.kafka_config)
                # Testa a conexão listando tópicos
                producer.list_topics(timeout=10)
                logger.info("Conexão com Kafka estabelecida")
                return producer
            except KafkaError as e:
                logger.warning(f"Tentativa {attempt + 1}/{max_retries} - Erro ao conectar no Kafka: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

    def get_eth_price(self):
        """Obtém preço ETH/USDC do Uniswap"""
        try:
            path = [
                self.w3.to_checksum_address(os.getenv('WETH_ADDRESS')),
                self.w3.to_checksum_address(os.getenv('USDC_ADDRESS'))
            ]
            
            amounts_out = self.uniswap_router.functions.getAmountsOut(
                self.w3.to_wei(1, 'ether'),
                path
            ).call()
            
            return self.w3.from_wei(amounts_out[-1], 'mwei')  # USDC tem 6 decimais
            
        except Exception as e:
            logger.error(f"Erro ao obter preço: {e}", exc_info=True)
            return None

    def send_to_kafka(self, message):
        """Envia mensagem para o Kafka com tratamento de erros"""
        try:
            future = self.producer.send(
                os.getenv('KAFKA_TOPIC', 'dex-prices'),
                value=message
            )
            # Força o envio imediato
            self.producer.flush()
            
            # Verifica se houve erro no envio
            if future.is_done and future.failed():
                raise future.exception()
                
            logger.info(f"Mensagem enviada: {message}")
            return True
            
        except Exception as e:
            logger.error(f"Falha ao enviar para Kafka: {e}")
            return False

    def start_streaming(self, interval=5):
        """Inicia o fluxo contínuo de coleta de preços"""
        logger.info(f"Iniciando coleta a cada {interval} segundos...")
        try:
            while True:
                start_time = time.time()
                
                price = self.get_eth_price()
                if price is not None:
                    message = {
                        'dex': 'Uniswap',
                        'pair': 'ETH/USDC',
                        'price': float(price),
                        'timestamp': int(time.time()),
                        'block_number': self.w3.eth.block_number
                    }
                    
                    self.send_to_kafka(message)
                
                # Calcula o tempo restante para manter o intervalo
                elapsed = time.time() - start_time
                sleep_time = max(0, interval - elapsed)
                time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            logger.info("Encerrando coletor...")
        finally:
            self.producer.close()
            logger.info("Producer Kafka fechado")

if __name__ == "__main__":
    try:
        collector = PriceCollector()
        collector.start_streaming()
    except Exception as e:
        logger.critical(f"Falha crítica: {e}", exc_info=True)
        exit(1)