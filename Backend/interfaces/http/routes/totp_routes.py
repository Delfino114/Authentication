from flask import Blueprint, request, jsonify, session, Response
from application.use_cases.totp_usecases import GenerateQRUseCase, ValidateTOTPUseCase
from interfaces.http.middleware.auth import login_required
import logging

logger = logging.getLogger(__name__)

totp_bp = Blueprint('totp', __name__)
generate_qr_use_case = GenerateQRUseCase()
validate_totp_use_case = ValidateTOTPUseCase()

@totp_bp.route('/qr', methods=['GET'])
@login_required
def get_qr():
    """Obtiene el código QR para TOTP"""
    try:
        email = session.get('email')
        logger.info(f"📷 Solicitando QR para: {email}")
        
        qr_image = generate_qr_use_case.execute(email)
        
        return Response(qr_image, mimetype='image/png')
        
    except Exception as e:
        logger.error(f"❌ Error generando QR: {e}")
        return jsonify({'error': 'Error generando código QR'}), 500

@totp_bp.route('/validate', methods=['POST'])
@login_required
def validate_totp():
    """Valida un código TOTP"""
    try:
        data = request.get_json()
        code = data.get('code')
        email = session.get('email')
        
        if not code or len(code) != 6:
            return jsonify({'error': 'Código de 6 dígitos requerido'}), 400
        
        logger.info(f"🔐 Validando TOTP para: {email}")
        
        is_valid = validate_totp_use_case.execute(email, code)
        
        if is_valid:
            # Actualizar sesión
            session['pending_2fa'] = False
            session['authenticated'] = True
            session['user_verified'] = True
            
            logger.info(f"✅ TOTP válido para: {email}")
            return jsonify({
                'valid': True,
                'message': 'Código TOTP válido'
            }), 200
        else:
            logger.warning(f"❌ TOTP inválido para: {email}")
            return jsonify({
                'valid': False,
                'error': 'Código TOTP inválido'
            }), 400
            
    except Exception as e:
        logger.error(f"❌ Error validando TOTP: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@totp_bp.route('/setup', methods=['POST'])
@login_required
def setup_totp():
    """Configura TOTP para un usuario"""
    try:
        from application.use_cases.totp_usecases import RegisterTOTPUseCase
        register_totp_use_case = RegisterTOTPUseCase()
        
        email = session.get('email')
        qr_uri = register_totp_use_case.execute(email)
        
        logger.info(f"🔐 TOTP configurado para: {email}")
        return jsonify({
            'success': True,
            'message': 'TOTP configurado exitosamente',
            'qr_uri': qr_uri
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error configurando TOTP: {e}")
        return jsonify({'error': 'Error configurando TOTP'}), 500

@totp_bp.route('/health', methods=['GET'])
def totp_health():
    """Health check para servicio TOTP"""
    try:
        from infrastructure.database.mongo_repository import MongoDBRepository
        mongo = MongoDBRepository()
        
        return jsonify({
            'status': 'OK',
            'service': 'TOTP/QR',
            'mongo_connected': mongo.client is not None
        }), 200
    except Exception as e:
        logger.error(f"❌ Error en health check TOTP: {e}")
        return jsonify({'status': 'ERROR', 'service': 'TOTP/QR'}), 500