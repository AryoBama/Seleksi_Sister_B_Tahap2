from .block import Block
from .pow import proof_of_work

class Blockchain:
    def __init__(self, difficulty=4):
        self.chain = []
        self.difficulty = difficulty
        self.create_genesis()

    def create_genesis(self):
        genesis = Block(0, [], "0")
        genesis.hash = genesis.compute_hash()
        self.chain.append(genesis)

    def last_block(self):
        return self.chain[-1]

    def add_block(self, block: Block):
        prev = self.last_block()
        if block.previous_hash != prev.hash:
            return False
        if not block.hash.startswith("0" * self.difficulty):
            return False
        self.chain.append(block)
        return True

    def mine_block(self, transactions):
        new_block = Block(len(self.chain), transactions, self.last_block().hash)
        proof_of_work(new_block, self.difficulty)
        self.add_block(new_block)
        return new_block

    def is_valid(self):
        for i in range(1, len(self.chain)):
            prev, cur = self.chain[i-1], self.chain[i]
            if cur.previous_hash != prev.hash:
                return False
            if cur.compute_hash() != cur.hash:
                return False
        return True