# Ruta: Backend/interfaces/http/routes/sms_routes.py
from flask import Blueprint, request, jsonify, session
from application.services.sms_service import SMSService
from interfaces.http.middleware.auth import login_required
import logging

logger = logging.getLogger(__name__)

sms_bp = Blueprint('sms', __name__)
sms_service = SMSService()

@sms_bp.route('/send-otp', methods=['POST'])
@login_required
def send_sms_otp():
    """Envía un OTP por SMS (endpoint específico para SMS)"""
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        email = session.get('email')
        
        if not phone_number:
            return jsonify({'error': 'Número de teléfono requerido'}), 400
        
        success, error = sms_service.send_otp(phone_number, email)
        
        if success:
            logger.info(f"✅ OTP enviado exitosamente a {phone_number}")
            return jsonify({
                'success': True,
                'message': 'OTP enviado exitosamente'
            }), 200
        else:
            return jsonify({'error': error or 'Error enviando OTP'}), 500
            
    except Exception as e:
        logger.error(f"❌ Error enviando OTP: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@sms_bp.route('/verify', methods=['POST'])
@login_required
def verify_sms_otp():
    """Verifica un OTP SMS (endpoint específico)"""
    try:
        data = request.get_json()
        otp = data.get('otp')
        email = session.get('email')
        
        if not otp:
            return jsonify({'error': 'OTP requerido'}), 400
        
        # Obtener teléfono del usuario desde la sesión o base de datos
        from application.use_cases.auth_usecases import GetUserInfoUseCase
        get_user_info_use_case = GetUserInfoUseCase()
        user_info, error = get_user_info_use_case.execute(email)
        
        if error:
            return jsonify({'error': error}), 404
        
        phone_number = user_info.get('phone_number') or session.get('phone_number')
        if not phone_number:
            return jsonify({'error': 'Número de teléfono no encontrado'}), 400
        
        is_valid, verify_error = sms_service.verify_otp(phone_number, otp, email)
        
        if is_valid:
            logger.info(f"✅ OTP SMS verificado: {email}")
            return jsonify({
                'valid': True,
                'message': 'OTP verificado exitosamente'
            }), 200
        else:
            return jsonify({
                'valid': False,
                'error': verify_error or 'OTP inválido'
            }), 400
            
    except Exception as e:
        logger.error(f"❌ Error verificando OTP SMS: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@sms_bp.route('/health', methods=['GET'])
def sms_health():
    """Health check para servicio SMS"""
    from infrastructure.external.twilio_adapter import TwilioAdapter
    from infrastructure.database.mongo_repository import MongoDBRepository
    
    try:
        twilio = TwilioAdapter()
        mongo = MongoDBRepository()
        
        return jsonify({
            'status': 'OK',
            'service': 'SMS OTP',
            'twilio_configured': twilio.client is not None,
            'mongo_connected': mongo.client is not None
        }), 200
    except Exception as e:
        logger.error(f"❌ Error en health check SMS: {e}")
        return jsonify({'status': 'ERROR', 'service': 'SMS OTP'}), 500