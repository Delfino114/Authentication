# Ruta: Backend/main.py
from flask import Flask
from flask_session import Session  # IMPORTAR Session
from config.settings import Config
from interfaces.http.middleware.cors import setup_cors
from interfaces.http.routes.auth_routes import auth_bp
from interfaces.http.routes.sms_routes import sms_bp
from interfaces.http.routes.totp_routes import totp_bp
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Configurar sesiones
    Session(app)
    
    # Configurar CORS
    setup_cors(app)
    
    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(sms_bp, url_prefix='/api/sms')
    app.register_blueprint(totp_bp, url_prefix='/api/totp')
    
    # Ruta de health check
    @app.route('/health')
    def health():
        return {
            'status': 'OK',
            'service': 'Unified Authentication System',
            'version': '1.0.0'
        }, 200
    
    # Ruta principal
    @app.route('/')
    def home():
        return {
            'message': 'Sistema de Autenticación Unificado',
            'endpoints': {
                'auth': '/api/auth',
                'sms': '/api/sms', 
                'totp': '/api/totp'
            }
        }, 200
    
    return app

if __name__ == '__main__':
    app = create_app()
    logger.info("🚀 Starting Unified Authentication System...")
    logger.info(f"📡 Server running on http://0.0.0.0:{Config.PORT}")
    logger.info("🔐 Available endpoints:")
    logger.info("   - POST /api/auth/register")
    logger.info("   - POST /api/auth/login")
    logger.info("   - POST /api/auth/verify-otp")
    logger.info("   - POST /api/auth/resend-otp")
    logger.info("   - GET  /api/auth/user-info")
    logger.info("   - POST /api/auth/logout")
    logger.info("   - GET  /api/totp/qr")
    logger.info("   - POST /api/totp/validate")
    
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=Config.PORT)