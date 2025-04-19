from web3 import Web3
import json
import os

class FlashLoanOrchestrator:
    def __init__(self, web3_provider, contract_address, contract_abi_path):
        self.web3 = web3_provider
        with open(contract_abi_path, 'r') as f:
            self.contract_abi = json.load(f)
        
        self.contract = self.web3.eth.contract(
            address=contract_address,
            abi=self.contract_abi
        )

    def execute_arbitrage(self, token_in, token_out, amount_wei, dex1, dex2):
        # 1. Preparar parâmetros
        params = self.web3.codec.encode_abi(
            ['address', 'address', 'address'],
            [dex1, dex2, token_out]
        )

        # 2. Chamar o contrato
        tx = self.contract.functions.requestFlashLoan(
            token_in,
            amount_wei,
            params
        ).build_transaction({
            'from': self.web3.eth.default_account,
            'gas': 1_000_000,
            'nonce': self.web3.eth.get_transaction_count(self.web3.eth.default_account)
        })

        # 3. Assinar e enviar
        signed_tx = self.web3.eth.account.sign_transaction(tx, os.getenv('PRIVATE_KEY'))
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return tx_hash.hex()