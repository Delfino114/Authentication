# Ruta: Backend/application/use_cases/totp_usecases.py
from domain.otp_generator import OTPGenerator
from infrastructure.database.mongo_repository import MongoDBRepository
from infrastructure.qr.qr_generator import QRGenerator
import logging

logger = logging.getLogger(__name__)

class GenerateQRUseCase:
    def __init__(self):
        self.qr_generator = QRGenerator()
        self.db_repo = MongoDBRepository()

    def execute(self, email: str) -> bytes:
        """Genera un código QR para TOTP"""
        try:
            user = self.db_repo.get_user(email)
            if not user or not user.get('secret'):
                raise Exception("Usuario no encontrado o sin secret configurado")
            
            secret = user['secret']
            otp = OTPGenerator(secret=secret)
            uri = otp.generate_uri(email, 'AuthSystem')
            
            qr_image = self.qr_generator.generate_qr_image(uri)
            logger.info(f"📷 QR generado para: {email}")
            return qr_image
            
        except Exception as e:
            logger.error(f"❌ Error en GenerateQRUseCase: {e}")
            raise

class RegisterTOTPUseCase:
    def __init__(self):
        self.db_repo = MongoDBRepository()

    def execute(self, email: str) -> str:
        """Registra un usuario para TOTP y genera secret"""
        try:
            otp = OTPGenerator()
            secret = otp.generate_secret()
            
            # Guardar secret en la base de datos
            self.db_repo.update_user(email, {'secret': secret})
            
            uri = otp.generate_uri(email, 'AuthSystem')
            logger.info(f"🔐 TOTP registrado para: {email}")
            return uri
            
        except Exception as e:
            logger.error(f"❌ Error en RegisterTOTPUseCase: {e}")
            raise

class ValidateTOTPUseCase:
    def __init__(self):
        self.db_repo = MongoDBRepository()

    def execute(self, email: str, code: str) -> bool:
        """Valida un código TOTP"""
        try:
            user = self.db_repo.get_user(email)
            if not user or not user.get('secret'):
                return False
            
            secret = user['secret']
            otp = OTPGenerator(secret=secret)
            is_valid = otp.verify_code(code)
            
            if is_valid:
                # Marcar usuario como verificado
                self.db_repo.update_user(email, {'verified': True})
                logger.info(f"✅ TOTP válido para: {email}")
            else:
                logger.warning(f"❌ TOTP inválido para: {email}")
                
            return is_valid
            
        except Exception as e:
            logger.error(f"❌ Error en ValidateTOTPUseCase: {e}")
            return False