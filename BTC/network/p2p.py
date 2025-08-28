import requests, threading

def broadcast_block(node, block):
    def worker():
        for peer in node.peers:
            try:
                requests.post(f"{peer}/block", json={"block": block.to_dict(), "node_url": node.url})
            except:
                pass
    threading.Thread(target=worker, daemon=True).start()

def request_chain(peer_url):
    try:
        r = requests.get(f"{peer_url}/chain", timeout=5)
        if r.status_code == 200:
            return r.json().get("chain", [])
    except:
        return []
    return []