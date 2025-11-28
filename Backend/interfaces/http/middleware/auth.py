# Ruta: Backend/interfaces/http/middleware/auth.py
from flask import session, jsonify, request
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def login_required(f):
    """Decorator para verificar que el usuario está autenticado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'email' not in session:
            logger.warning("🔒 Intento de acceso no autorizado")
            return jsonify({'error': 'Se requiere autenticación'}), 401
        return f(*args, **kwargs)
    return decorated_function

def auth_method_required(auth_method):
    """Decorator para verificar el método de autenticación"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if session.get('auth_method') != auth_method:
                logger.warning(f"❌ Método de autenticación incorrecto. Esperado: {auth_method}, Obtenido: {session.get('auth_method')}")
                return jsonify({'error': f'Método de autenticación {auth_method} requerido'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_2fa(f):
    """Decorator para verificar que se requiere 2FA"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('pending_2fa', False):
            logger.warning("❌ 2FA no pendiente")
            return jsonify({'error': 'Verificación 2FA requerida'}), 403
        return f(*args, **kwargs)
    return decorated_function

def check_session():
    """Middleware para verificar y loguear la sesión"""
    logger.debug(f"🔍 Verificando sesión: {dict(session)}")
    return 'email' in session