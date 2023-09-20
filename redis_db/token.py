import redis
    
def add_token(rd: redis.Redis, key: str, value: str, ttl: int):
    rd.setex(key, ttl, value)
    
def delete_token(rd: redis.Redis, key_to_delete: str):
    rd.delete(key_to_delete)
    
def add_revoked_token(rd: redis.Redis, key: str, ttl: int):
    value = "revoke"
    if ttl < 0:
        ttl = 1
    rd.setex(key, ttl, value)
    
def check_revoked_token(rd: redis.Redis, token_str: str) -> bool:
    # Get the value associated with the key
    bytes_value = rd.get(token_str)
    if bytes_value is not None:
        string_value = bytes_value.decode('utf-8')
        if string_value == "revoke":
            return True
    return False