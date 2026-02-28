import bcrypt

def hash_password(password: str) -> str:
    """Cria o hash do password"""
    
    hashed_bytes = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    return hashed_bytes.decode('utf-8')

def check_password(password: str, hashed_password: str) -> bool:
    """Compara hashs entre texto plano e password codificado"""
    
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))