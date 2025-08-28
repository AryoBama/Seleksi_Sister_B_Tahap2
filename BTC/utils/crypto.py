import hashlib, json

def sha256_hex(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()

def json_dumps(obj) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))