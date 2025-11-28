# Ruta: Backend/interfaces/http/middleware/cors.py
from flask_cors import CORS
from config.settings import Config
import logging

logger = logging.getLogger(__name__)

def setup_cors(app):
    """Configura CORS para la aplicación Flask"""
    CORS(app, 
         origins=Config.CORS_ORIGINS,
         supports_credentials=True,
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"]
    )
    
    # Headers CORS adicionales
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    logger.info("✅ CORS configurado correctamente")
    logger.info(f"🌐 Orígenes permitidos: {Config.CORS_ORIGINS}")