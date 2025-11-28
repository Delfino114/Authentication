import pyotp
import logging

logger = logging.getLogger(__name__)

class OTPGenerator:
    def __init__(self, secret=None):
        self.secret = secret or pyotp.random_base32()

    def generate_secret(self) -> str:
        """Genera un nuevo secret para TOTP"""
        self.secret = pyotp.random_base32()
        logger.info("🔑 Nuevo secret generado")
        return self.secret

    def generate_uri(self, usr_email: str, issuer_name: str) -> str:
        """Genera la URI para el código QR"""
        if not self.secret:
            raise ValueError("Secret no configurado")
        
        totp = pyotp.TOTP(self.secret)
        uri = totp.provisioning_uri(usr_email, issuer_name)
        logger.info(f"📷 URI generada para: {usr_email}")
        return uri

    def verify_code(self, code: str) -> bool:
        """Verifica un código TOTP"""
        if not self.secret:
            raise ValueError("Secret no configurado")
        
        totp = pyotp.TOTP(self.secret)
        is_valid = totp.verify(code)
        
        if is_valid:
            logger.info("✅ Código TOTP válido")
        else:
            logger.warning("❌ Código TOTP inválido")
            
        return is_valid

    def get_current_code(self) -> str:
        """Obtiene el código TOTP actual"""
        if not self.secret:
            raise ValueError("Secret no configurado")
        
        totp = pyotp.TOTP(self.secret)
        return totp.now()