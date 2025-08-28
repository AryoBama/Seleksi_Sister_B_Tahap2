from datetime import datetime
from ..utils.crypto import json_dumps, sha256_hex

class Block:
    def __init__(self, index, transactions, previous_hash, nonce=0, timestamp=None, hash = None):
        self.index = index
        self.timestamp = timestamp or datetime.utcnow().isoformat()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = hash or self.compute_hash()

    def compute_hash(self):
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
        }
        return sha256_hex(json_dumps(block_content))

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": self.transactions,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash,
        }