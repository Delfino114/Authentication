# Ruta: Backend/interfaces/http/routes/auth_routes.py
from flask import Blueprint, request, jsonify, session
from application.use_cases.auth_usecases import RegisterUserUseCase, AuthenticateUserUseCase, GetUserInfoUseCase
from application.use_cases.totp_usecases import RegisterTOTPUseCase
from application.services.sms_service import SMSService
from interfaces.http.middleware.auth import login_required
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint('auth', __name__)
register_use_case = RegisterUserUseCase()
authenticate_use_case = AuthenticateUserUseCase()
get_user_info_use_case = GetUserInfoUseCase()
register_totp_use_case = RegisterTOTPUseCase()
sms_service = SMSService()

@auth_bp.route('/register', methods=['POST'])
def register():
    """Registra un nuevo usuario"""
    try:
        data = request.get_json()
        logger.info("=" * 50)
        logger.info("📝 REGISTRO - Datos recibidos:")
        logger.info(f"   Email: {data.get('email')}")
        logger.info(f"   Método: {data.get('auth_method')}")
        logger.info("=" * 50)
        
        email = data.get('email')
        password = data.get('password')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        auth_method = data.get('auth_method', 'totp')
        phone_number = data.get('phone_number')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        # Registrar usuario
        user, error = register_use_case.execute(
            email, password, first_name, last_name, auth_method, phone_number
        )
        
        if error:
            return jsonify({'error': error}), 400
        
        # Configurar sesión
        session.permanent = True
        session['email'] = email
        session['first_name'] = first_name
        session['auth_method'] = auth_method
        session['pending_2fa'] = True
        
        if auth_method == 'sms':
            # Enviar OTP por SMS
            if not phone_number:
                return jsonify({'error': 'Número de teléfono requerido para SMS'}), 400
            
            success, sms_error = sms_service.send_otp(phone_number, email)
            
            if success:
                session['phone_number'] = phone_number
                logger.info(f"✅ Usuario SMS registrado: {email}")
                return jsonify({
                    'success': True,
                    'message': 'Usuario registrado. OTP enviado por SMS.',
                    'requires_otp': True,
                    'auth_method': 'sms'
                }), 200
            else:
                return jsonify({'error': sms_error or 'Error enviando OTP'}), 500
        
        elif auth_method == 'totp':
            # Generar secret y QR para TOTP
            try:
                qr_uri = register_totp_use_case.execute(email)
                logger.info(f"✅ Usuario TOTP registrado: {email}")
                return jsonify({
                    'success': True,
                    'message': 'Usuario registrado. Configure TOTP.',
                    'requires_otp': True,
                    'auth_method': 'totp',
                    'qr_uri': qr_uri
                }), 200
            except Exception as e:
                logger.error(f"❌ Error registrando TOTP: {e}")
                return jsonify({'error': 'Error configurando TOTP'}), 500
        
    except Exception as e:
        logger.error(f"❌ Error en registro: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Inicia sesión de usuario"""
    try:
        data = request.get_json()
        logger.info("=" * 50)
        logger.info("🔐 LOGIN - Datos recibidos:")
        logger.info(f"   Email: {data.get('email')}")
        logger.info("=" * 50)
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email y contraseña requeridos'}), 400
        
        # Autenticar usuario
        user, error = authenticate_use_case.execute(email, password)
        
        if error:
            return jsonify({'error': error}), 401
        
        # Configurar sesión
        session.permanent = True
        session['email'] = email
        session['first_name'] = user.get('first_name', '')
        session['auth_method'] = user.get('auth_method', 'totp')
        
        auth_method = user.get('auth_method', 'totp')
        requires_otp = user.get('requires_otp', True)
        
        if auth_method == 'sms' and requires_otp:
            # Enviar OTP por SMS
            phone_number = user.get('phone_number')
            if not phone_number:
                return jsonify({'error': 'Número de teléfono no configurado'}), 400
            
            session['phone_number'] = phone_number
            session['pending_2fa'] = True
            
            success, sms_error = sms_service.send_otp(phone_number, email)
            
            if success:
                logger.info(f"✅ Login SMS exitoso: {email}")
                return jsonify({
                    'success': True,
                    'requires_otp': True,
                    'auth_method': 'sms',
                    'message': 'OTP enviado a tu teléfono'
                }), 200
            else:
                return jsonify({'error': sms_error or 'Error enviando OTP'}), 500
        
        elif auth_method == 'totp' and requires_otp:
            # Requiere verificación TOTP
            session['pending_2fa'] = True
            logger.info(f"✅ Login TOTP exitoso (pendiente verificación): {email}")
            return jsonify({
                'success': True,
                'requires_otp': True,
                'auth_method': 'totp',
                'message': 'Verificación TOTP requerida'
            }), 200
        else:
            # Login directo (sin 2FA)
            session['pending_2fa'] = False
            session['authenticated'] = True
            logger.info(f"✅ Login directo exitoso: {email}")
            return jsonify({
                'success': True,
                'requires_otp': False,
                'auth_method': auth_method,
                'message': 'Login exitoso'
            }), 200
        
    except Exception as e:
        logger.error(f"❌ Error en login: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/verify-otp', methods=['POST'])
def verify_otp():
    """Verifica un OTP para SMS"""
    try:
        data = request.get_json()
        otp = data.get('otp')
        email = data.get('email') or session.get('email')
        
        if not otp or not email:
            return jsonify({'error': 'OTP y email requeridos'}), 400
        
        # Obtener teléfono del usuario
        user_info, error = get_user_info_use_case.execute(email)
        if error:
            return jsonify({'error': error}), 404
        
        phone_number = user_info.get('phone_number') or session.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Número de teléfono no encontrado'}), 400
        
        # Verificar OTP
        is_valid, verify_error = sms_service.verify_otp(phone_number, otp, email)
        
        if is_valid:
            # Actualizar sesión
            session['pending_2fa'] = False
            session['authenticated'] = True
            session['user_verified'] = True
            
            logger.info(f"✅ OTP verificado exitosamente: {email}")
            return jsonify({
                'valid': True,
                'message': 'OTP verificado exitosamente',
                'authenticated': True
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': verify_error or 'OTP inválido'
            }), 400
        
    except Exception as e:
        logger.error(f"❌ Error verificando OTP: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/resend-otp', methods=['POST'])
def resend_otp():
    """Reenvía un OTP por SMS"""
    try:
        data = request.get_json()
        email = data.get('email') or session.get('email')
        
        if not email:
            return jsonify({'error': 'Email requerido'}), 400
        
        # Obtener información del usuario
        user_info, error = get_user_info_use_case.execute(email)
        if error:
            return jsonify({'error': error}), 404
        
        phone_number = user_info.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Número de teléfono no encontrado'}), 400
        
        # Reenviar OTP
        success, sms_error = sms_service.resend_otp(phone_number, email)
        
        if success:
            logger.info(f"✅ OTP reenviado: {email}")
            return jsonify({'message': 'OTP reenviado exitosamente'}), 200
        else:
            return jsonify({'error': sms_error or 'Error reenviando OTP'}), 500
        
    except Exception as e:
        logger.error(f"❌ Error reenviando OTP: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/user-info', methods=['GET'])
@login_required
def user_info():
    """Obtiene información del usuario autenticado"""
    try:
        email = session.get('email')
        user_info, error = get_user_info_use_case.execute(email)
        
        if error:
            return jsonify({'error': error}), 404
        
        logger.info(f"📋 Información de usuario obtenida: {email}")
        return jsonify(user_info), 200
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo información de usuario: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/session-check', methods=['GET'])
def session_check():
    """Verifica el estado de la sesión"""
    return jsonify({
        'logged_in': 'email' in session,
        'email': session.get('email'),
        'auth_method': session.get('auth_method'),
        'pending_2fa': session.get('pending_2fa', False),
        'authenticated': session.get('authenticated', False)
    }), 200

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Cierra la sesión del usuario"""
    try:
        email = session.get('email')
        session.clear()
        logger.info(f"✅ Logout exitoso: {email}")
        return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'}), 200
    except Exception as e:
        logger.error(f"❌ Error en logout: {e}")
        return jsonify({'error': 'Error cerrando sesión'}), 500