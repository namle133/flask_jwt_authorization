import jwt as JWT
from datetime import datetime
import os

# Your JWT secret key (the same key used for encoding)
jwt_secret_key = os.getenv("SECRET_KEY")

def get_current_timestamp() -> int:
    time_now = int(datetime.timestamp(datetime.now()))
    return time_now

def calculate_time_to_live(token: str) -> int:
    # Decode the access token
    decoded_token = JWT.decode(token , jwt_secret_key, algorithms=["HS256"])
    # Extract the expiration time ('exp' claim) as a Unix timestamp
    expiration_timestamp = decoded_token.get('exp')
    # Calculate the value of time to live
    current_timestamp = get_current_timestamp()
    ttl = int(expiration_timestamp) - current_timestamp
    
    return ttl