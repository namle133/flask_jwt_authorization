import random

LENGTH_VERIFICATION_CODE = 6

def generate_random_number():
    """
    Generate a random number with the specified length.

    Args:
        length (int): The length of the random number.

    Returns:
        str: A random number with the specified length.
    """
    if LENGTH_VERIFICATION_CODE <= 0:
        raise ValueError("Length must be greater than 0")

    # Generate a random digit for each position in the number
    random_digits = [str(random.randint(0, 9)) for _ in range(LENGTH_VERIFICATION_CODE)]

    # Join the random digits to form the final random number
    random_number = ''.join(random_digits)

    return random_number
