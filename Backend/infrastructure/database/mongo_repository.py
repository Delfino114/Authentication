from pymongo import MongoClient
import os
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

class MongoDBRepository:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None
        self.connect()
    
    def connect(self):
        """Establece conexión con MongoDB"""
        try:
            logger.info("🔗 Conectando a MongoDB Atlas...")
            self.client = MongoClient(Config.MONGODB_URI)
            
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client[Config.MONGODB_DB_NAME]
            self.collection = self.db['users']
            
            logger.info(f"✅ Conectado a MongoDB Atlas: {Config.MONGODB_DB_NAME}.users")
            
            # Verificar que podemos hacer operaciones
            count = self.collection.count_documents({})
            logger.info(f"📊 Total de usuarios en BD: {count}")
            
        except Exception as e:
            logger.error(f"❌ ERROR conectando a MongoDB Atlas: {e}")
            raise

    def save_user(self, email, user_data):
        """Guarda o actualiza un usuario"""
        try:
            user_data['updated_at'] = os.times().elapsed
            
            result = self.collection.update_one(
                {'email': email},
                {'$set': user_data},
                upsert=True
            )
            logger.info(f"💾 Usuario guardado/actualizado: {email}")
            return result.upserted_id or result.modified_count > 0
        except Exception as e:
            logger.error(f"❌ Error guardando usuario: {e}")
            return False

    def get_user(self, email):
        """Obtiene un usuario por email"""
        try:
            user = self.collection.find_one({'email': email})
            if user:
                logger.debug(f"🔍 Usuario encontrado: {email}")
            else:
                logger.debug(f"🔍 Usuario NO encontrado: {email}")
            return user
        except Exception as e:
            logger.error(f"❌ Error buscando usuario: {e}")
            return None

    def update_user(self, email, updates):
        """Actualiza un usuario"""
        try:
            updates['updated_at'] = os.times().elapsed
            
            result = self.collection.update_one(
                {'email': email},
                {'$set': updates}
            )
            success = result.modified_count > 0
            if success:
                logger.info(f"✏️ Usuario actualizado: {email}")
            return success
        except Exception as e:
            logger.error(f"❌ Error actualizando usuario: {e}")
            return False

    def user_exists(self, email):
        """Verifica si un usuario existe"""
        try:
            exists = self.collection.count_documents({'email': email}) > 0
            logger.debug(f"🔎 Usuario existe {email}: {exists}")
            return exists
        except Exception as e:
            logger.error(f"❌ Error verificando usuario: {e}")
            return False

    def get_user_secret(self, email):
        """Obtiene el secret TOTP de un usuario"""
        try:
            user = self.get_user(email)
            return user.get('secret') if user else None
        except Exception as e:
            logger.error(f"❌ Error obteniendo secret: {e}")
            return None

    def set_user_secret(self, email, secret):
        """Establece el secret TOTP de un usuario"""
        try:
            return self.update_user(email, {'secret': secret})
        except Exception as e:
            logger.error(f"❌ Error estableciendo secret: {e}")
            return False