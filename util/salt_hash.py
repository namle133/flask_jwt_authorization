import bcrypt

# Function to hash a password with a randomly generated salt
def hash_password(password: str) -> bytes:
    # Generate a random salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

# Function to verify a password
def verify_password(plain_password: str, hashed_password: bytes) -> bool:
    plain_pwd_bytes = plain_password.encode('utf-8')
    # Check if the provided plain password matches the hashed password
    return bcrypt.checkpw(plain_pwd_bytes, hashed_password)
