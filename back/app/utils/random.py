import string
import random

def generate_random_hash(
    size=12, 
    chars=string.ascii_uppercase + string.ascii_lowercase + string.digits
):
    """Gera uma string aleatória"""
    
    return ''.join(random.choice(chars) for _ in range(size))