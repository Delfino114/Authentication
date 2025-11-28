# Ruta: Backend/application/use_cases/auth_usecases.py
from application.services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

class RegisterUserUseCase:
    def __init__(self):
        self.auth_service = AuthService()
    
    def execute(self, email, password, first_name, last_name, auth_method, phone_number=None):
        """Caso de uso para registrar un usuario"""
        logger.info(f"📝 Registrando usuario: {email}")
        return self.auth_service.register_user(email, password, first_name, last_name, auth_method, phone_number)

class AuthenticateUserUseCase:
    def __init__(self):
        self.auth_service = AuthService()
    
    def execute(self, email, password):
        """Caso de uso para autenticar un usuario"""
        logger.info(f"🔐 Autenticando usuario: {email}")
        return self.auth_service.authenticate_user(email, password)

class GetUserInfoUseCase:
    def __init__(self):
        self.auth_service = AuthService()
    
    def execute(self, email):
        """Caso de uso para obtener información del usuario"""
        logger.info(f"📋 Obteniendo información de: {email}")
        return self.auth_service.get_user_info(email)