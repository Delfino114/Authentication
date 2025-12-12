# Ruta: Backend/application/services/auth_service.py
from infrastructure.database.mongo_repository import MongoDBRepository
from domain.models import User
import logging

logger = logging.getLogger(__name__)

class AuthService:
    def __init__(self):
        
        self.db_repo = MongoDBRepository()
    
    def register_user(self, email, password, first_name, last_name, auth_method, phone_number=None):
        """Registra un nuevo usuario en el sistema"""
        try:
            # Verificar si el usuario ya existe
            if self.db_repo.user_exists(email):
                return None, "El usuario ya existe"
            
            # Crear objeto usuario
            user_data = {
                'email': email,
                'password': password,
                'first_name': first_name,
                'last_name': last_name,
                'auth_method': auth_method,
                'phone_number': phone_number,
                'verified': False,
                'secret': None
            }
            
            # Guardar usuario
            if auth_method == 'totp':
                # Para TOTP, el secret se generará después
                user_data['requires_otp'] = True
            elif auth_method == 'sms':
                user_data['requires_otp'] = True
                user_data['verified'] = False
            
            success = self.db_repo.save_user(email, user_data)
            
            if success:
                logger.info(f"✅ Usuario registrado: {email}")
                return user_data, None
            else:
                return None, "Error al guardar el usuario"
                
        except Exception as e:
            logger.error(f"❌ Error en register_user: {e}")
            return None, str(e)
    
    def authenticate_user(self, email, password):
        """Autentica un usuario con email y contraseña"""
        try:
            user = self.db_repo.get_user(email)
            
            if not user:
                return None, "Usuario no encontrado"
            
            if user.get('password') != password:
                return None, "Contraseña incorrecta"
            
            logger.info(f"✅ Usuario autenticado: {email}")
            return user, None
            
        except Exception as e:
            logger.error(f"❌ Error en authenticate_user: {e}")
            return None, str(e)
    
    def get_user_info(self, email):
        """Obtiene información del usuario"""
        try:
            user = self.db_repo.get_user(email)
            if user:
                return {
                    'email': user.get('email'),
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                    'auth_method': user.get('auth_method', 'totp'),
                    'verified': user.get('verified', False)
                }, None
            return None, "Usuario no encontrado"
        except Exception as e:
            logger.error(f"❌ Error en get_user_info: {e}")
            return None, str(e)
    
    def get_user_info(self, email):
        """Obtiene información del usuario"""
        try:
            logger.info(f"🔍 Buscando usuario en BD: {email}")
            user = self.db_repo.get_user(email)
            
            if user:
                logger.info(f"✅ Usuario encontrado: {email}")
                logger.info(f"📋 Datos del usuario: {user}")
                return {
                    'email': user.get('email'),
                    'first_name': user.get('first_name'),
                    'last_name': user.get('last_name'),
                    'auth_method': user.get('auth_method', 'totp'),
                    'phone_number': user.get('phone_number'),  # AÑADIR ESTO
                    'verified': user.get('verified', False)
                }, None
            logger.warning(f"❌ Usuario no encontrado: {email}")
            return None, "Usuario no encontrado"
        except Exception as e:
            logger.error(f"❌ Error en get_user_info: {e}")
            return None, str(e)