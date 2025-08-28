class TransactionPool:
    def __init__(self):
        self.pool = []

    def add(self, tx: dict):
        self.pool.append(tx)

    def get_all(self):
        return self.pool.copy()

    def clear(self):
        self.pool = []