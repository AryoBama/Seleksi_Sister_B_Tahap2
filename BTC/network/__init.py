class Node:
    def __init__(self, url):
        self.url = url
        self.peers = set()

    def register_peers(self, peers):
        for p in peers:
            self.peers.add(p.rstrip("/"))