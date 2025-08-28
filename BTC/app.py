from flask import Flask, request, jsonify
from .blockchain.chain import Blockchain
from .blockchain.block import Block
from .transactions.pool import TransactionPool
from .network.node import Node
from .network.p2p import broadcast_block, request_chain

import argparse

app = Flask(__name__)

blockchain = None
tx_pool = TransactionPool()
node = None

@app.route("/transaction", methods=["POST"])
def add_tx():
    tx = request.get_json()
    tx_pool.add(tx)
    return jsonify({"message": "tx added", "tx": tx})

@app.route("/transactions", methods=["GET"])
def get_tx():
    return jsonify({"pool": tx_pool.get_all()})

@app.route("/mine", methods=["GET"])
def mine():
    if not tx_pool.get_all():
        return jsonify({"message": "no tx to mine"}), 400
    block = blockchain.mine_block(tx_pool.get_all())
    tx_pool.clear()
    broadcast_block(node, block)
    return jsonify({"block": block.to_dict()})

@app.route("/chain", methods=["GET"])
def get_chain():
    return jsonify({"chain": [b.to_dict() for b in blockchain.chain]})

@app.route("/block", methods=["POST"])
def receive_block():
    data = request.get_json()
    blk_data = data["block"]
    b = Block(blk_data["index"], blk_data["transactions"], blk_data["previous_hash"],
              blk_data["nonce"], blk_data["timestamp"])
    b.hash = blk_data["hash"]
    if blockchain.add_block(b):
        return jsonify({"message": "block accepted"})
    else:
        # fallback sync
        for peer in node.peers:
            remote = request_chain(peer)
            if remote and len(remote) > len(blockchain.chain):
                blockchain.chain = [Block(**blk) for blk in remote]
                return jsonify({"message": "chain replaced"}), 200
        return jsonify({"message": "block rejected"}), 400

@app.route("/nodes/register", methods=["POST"])
def register_nodes():
    peers = request.get_json().get("nodes", [])
    node.register_peers(peers)
    return jsonify({"peers": list(node.peers)})

@app.route("/sync", methods=["GET"])
def sync_chain():
    longest_chain = blockchain.chain
    for peer in node.peers:
        remote = request_chain(peer)
        if remote and len(remote) > len(longest_chain):
            longest_chain = [Block(**blk) for blk in remote]

    if len(longest_chain) > len(blockchain.chain):
        blockchain.chain = longest_chain
        return jsonify({"message": "chain updated", "length": len(longest_chain)})
    else:
        return jsonify({"message": "chain already up-to-date", "length": len(blockchain.chain)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--peers", default="")
    parser.add_argument("--difficulty", type=int, default=4)
    args = parser.parse_args()

    blockchain = Blockchain(args.difficulty)
    node = Node(f"http://127.0.0.1:{args.port}")
    if args.peers:
        node.register_peers(args.peers.split(","))

    app.run(port=args.port)

