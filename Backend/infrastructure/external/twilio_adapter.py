from twilio.rest import Client
import os
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class TwilioAdapter:
    def __init__(self):
        self.account_sid = Config.TWILIO_ACCOUNT_SID
        self.auth_token = Config.TWILIO_AUTH_TOKEN
        self.phone_number = Config.TWILIO_FROM_NUMBER
        
        logger.info(f"🔧 Twilio Config:")
        logger.info(f"   Account SID: {self.account_sid}")
        logger.info(f"   Auth Token: {self.auth_token[:10]}...")
        logger.info(f"   Phone: {self.phone_number}")
        
        if not all([self.account_sid, self.auth_token, self.phone_number]):
            logger.error("❌ FALTAN CREDENCIALES DE TWILIO")
            self.client = None
            return
        
        try:
            self.client = Client(self.account_sid, self.auth_token)
            logger.info("✅ Cliente Twilio inicializado correctamente")
        except Exception as e:
            logger.error(f"❌ Error inicializando Twilio: {e}")
            self.client = None

    def send_otp(self, phone_number: str, otp: str) -> bool:
        """Envía un OTP por SMS usando Twilio"""
        try:
            if not self.client:
                logger.error("❌ Cliente Twilio no disponible")
                return False
                
            logger.info("=" * 50)
            logger.info("📤 ENVIANDO SMS CON TWILIO:")
            logger.info(f"   FROM: {self.phone_number}")
            logger.info(f"   TO: {phone_number}")
            logger.info(f"   OTP: {otp}")
            logger.info("=" * 50)
            
            if not self._is_valid_phone_number(phone_number):
                return False
            
            # ENVIAR SMS
            message = self.client.messages.create(
                body=f'Tu código de verificación es: {otp}',
                from_=self.phone_number,
                to=phone_number
            )
            
            logger.info(f"✅ SMS ENVIADO EXITOSAMENTE!")
            logger.info(f"   SID: {message.sid}")
            logger.info(f"   Status: {message.status}")
            logger.info("=" * 50)
            
            return True
            
        except Exception as e:
            logger.error(f"❌ ERROR ENVIANDO SMS: {e}")
            logger.info("=" * 50)
            return False
    
    def _is_valid_phone_number(self, phone_number):
        """Valida el formato del número"""
        if not phone_number:
            return False
        if not phone_number.startswith('+'):
            return False
        digits = phone_number[1:]
        if not digits.isdigit():
            return False
        if len(digits) < 10 or len(digits) > 15:
            return False
        return True