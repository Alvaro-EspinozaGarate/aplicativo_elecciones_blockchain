import hashlib
import json, os
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Cargar blockchain previa si existe
        if os.path.exists('blockchain.json'):
            with open('blockchain.json', 'r') as f:
                self.chain = json.load(f)
        else:
            # Crear bloque génesis
            self.new_block(previous_hash='1', proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, usuario, candidato):
        self.current_transactions.append({
            'usuario': usuario,
            'candidato': candidato,
            'timestamp': time()
        })
        return self.last_block['index'] + 1
    
    def add_vote(self, usuario, rector, vicerrector):
        self.current_transactions.append({
            "usuario": usuario,
            "rector": rector,
            "vicerrector": vicerrector,
            "timestamp": time()
        })


    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        return self.chain[-1]
