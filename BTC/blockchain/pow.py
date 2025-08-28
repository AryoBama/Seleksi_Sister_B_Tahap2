from .block import Block
from ..utils.crypto import sha256_hex

def merkle_root(transactions):
    if not transactions:
        return sha256_hex("")
    nodes = [sha256_hex(str(tx)) for tx in transactions]
    while len(nodes) > 1:
        if len(nodes) % 2 == 1:
            nodes.append(nodes[-1])
        nodes = [sha256_hex(nodes[i] + nodes[i+1]) for i in range(0, len(nodes), 2)]
    return nodes[0]

def proof_of_work(block: Block, difficulty: int):
    target = "0" * difficulty
    nonce = 0
    while True:
        block.nonce = nonce
        h = block.compute_hash()
        if h.startswith(target):
            block.hash = h
            return block
        nonce += 1
