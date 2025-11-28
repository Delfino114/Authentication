import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)

def validate_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    is_valid = bool(re.match(pattern, email))
    if not is_valid:
        logger.warning(f"❌ Email inválido: {email}")
    return is_valid

def validate_phone_number(phone: str) -> bool:
    """Valida formato de número de teléfono"""
    # Formato internacional: +521234567890
    pattern = r'^\+\d{10,15}$'
    is_valid = bool(re.match(pattern, phone))
    if not is_valid:
        logger.warning(f"❌ Teléfono inválido: {phone}")
    return is_valid

def sanitize_input(text: str) -> str:
    """Limpia y sanitiza input de usuario"""
    if not text:
        return text
    
    # Remover espacios en blanco extras
    text = text.strip()
    
    # Limitar longitud
    if len(text) > 255:
        text = text[:255]
        logger.warning("⚠️ Input truncado por longitud")
    
    return text

def generate_random_code(length: int = 6) -> str:
    """Genera un código aleatorio numérico"""
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(length)])

def format_response(success: bool, message: str, data: Optional[dict] = None) -> dict:
    """Formatea una respuesta estándar"""
    response = {
        'success': success,
        'message': message
    }
    
    if data:
        response.update(data)
    
    return response