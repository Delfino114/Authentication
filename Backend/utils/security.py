# Ruta: Backend/utils/security.py
import hashlib
import secrets
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    """Hashea una contraseña (en producción usar bcrypt)"""
    # NOTA: En producción usar bcrypt o argon2
    # Esto es solo para demostración
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt.encode('utf-8'),
        100000  # iterations
    )
    return f"{salt}${hashed.hex()}"

def verify_password(password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    try:
        salt, stored_hash = hashed_password.split('$')
        new_hash = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt.encode('utf-8'),
            100000
        ).hex()
        
        return secrets.compare_digest(new_hash, stored_hash)
    except Exception as e:
        logger.error(f"❌ Error verificando contraseña: {e}")
        return False

def generate_session_token() -> str:
    """Genera un token de sesión seguro"""
    return secrets.token_urlsafe(32)

def validate_otp_code(code: str) -> bool:
    """Valida que un código OTP tenga el formato correcto"""
    if not code or len(code) != 6:
        return False
    
    return code.isdigit()