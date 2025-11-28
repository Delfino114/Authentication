# Ruta: Backend/application/services/sms_service.py
from infrastructure.external.twilio_adapter import TwilioAdapter
from application.use_cases.sms_usecases import SendOTPUseCase, VerifyOTPUseCase
from infrastructure.database.mongo_repository import MongoDBRepository
import logging

logger = logging.getLogger(__name__)

class SMSService:
    def __init__(self):
        self.twilio_adapter = TwilioAdapter()
        self.db_repo = MongoDBRepository()
        self.send_otp_use_case = SendOTPUseCase(self.twilio_adapter, self.db_repo)
        self.verify_otp_use_case = VerifyOTPUseCase(self.db_repo)
    
    def send_otp(self, phone_number, email=None):
        """Envía un OTP por SMS"""
        try:
            logger.info(f"📤 Enviando OTP a: {phone_number}")
            
            success = self.send_otp_use_case.execute(phone_number)
            
            if success and email:
                # Actualizar estado del usuario
                self.db_repo.update_user(email, {'pending_verification': True})
            
            return success, None
            
        except Exception as e:
            logger.error(f"❌ Error en send_otp: {e}")
            return False, str(e)
    
    def verify_otp(self, phone_number, otp, email=None):
        """Verifica un OTP"""
        try:
            logger.info(f"🔍 Verificando OTP para: {phone_number}")
            
            is_valid = self.verify_otp_use_case.execute(phone_number, otp)
            
            if is_valid and email:
                # Marcar usuario como verificado
                self.db_repo.update_user(email, {
                    'verified': True,
                    'pending_verification': False
                })
            
            return is_valid, None
            
        except Exception as e:
            logger.error(f"❌ Error en verify_otp: {e}")
            return False, str(e)
    
    def resend_otp(self, phone_number, email=None):
        """Reenvía un OTP"""
        try:
            logger.info(f"🔄 Reenviando OTP a: {phone_number}")
            return self.send_otp(phone_number, email)
        except Exception as e:
            logger.error(f"❌ Error en resend_otp: {e}")
            return False, str(e)