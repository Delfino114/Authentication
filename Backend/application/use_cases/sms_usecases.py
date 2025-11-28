from domain.sms_otp_generator import SMSOTPGenerator
import logging

logger = logging.getLogger(__name__)

class SendOTPUseCase:
    def __init__(self, sms_adapter, mongo_repository):
        self.sms_adapter = sms_adapter
        self.otp_generator = SMSOTPGenerator(mongo_repository)

    def execute(self, phone_number: str) -> bool:
        """Envía un OTP por SMS"""
        try:
            otp = self.otp_generator.generate_otp(phone_number)
            result = self.sms_adapter.send_otp(phone_number, otp)
            logger.info(f"📨 OTP enviado a {phone_number}: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ Error en SendOTPUseCase: {e}")
            return False

class VerifyOTPUseCase:
    def __init__(self, mongo_repository):
        self.otp_generator = SMSOTPGenerator(mongo_repository)

    def execute(self, phone_number: str, otp: str) -> bool:
        """Verifica un OTP"""
        try:
            result = self.otp_generator.verify_otp(phone_number, otp)
            logger.info(f"🔍 Verificación OTP para {phone_number}: {result}")
            return result
        except Exception as e:
            logger.error(f"❌ Error en VerifyOTPUseCase: {e}")
            return False