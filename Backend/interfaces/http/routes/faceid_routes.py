from flask import Blueprint, request, jsonify, session
from domain.face_recognizer import FaceRecognizer
from interfaces.http.middleware.auth import login_required
import logging
import os

logger = logging.getLogger(__name__)

faceid_bp = Blueprint('faceid', __name__)
face_recognizer = FaceRecognizer()

# Directorio para almacenar imágenes temporalmente
UPLOAD_FOLDER = 'temp_uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@faceid_bp.route('/register', methods=['POST'])
@login_required
def register_face():
    """Registra un rostro para Face ID"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Imagen requerida'}), 400
        
        image_file = request.files['image']
        email = session.get('email')
        
        if image_file.filename == '':
            return jsonify({'error': 'Archivo no seleccionado'}), 400
        
        # Guardar imagen temporalmente
        image_path = os.path.join(UPLOAD_FOLDER, f"{email}_face.jpg")
        image_file.save(image_path)
        
        # Registrar rostro
        success = face_recognizer.register_face(image_path, email)
        
        # Limpiar archivo temporal
        try:
            os.remove(image_path)
        except:
            pass
        
        if success:
            logger.info(f"✅ Rostro registrado para: {email}")
            return jsonify({
                'success': True,
                'message': 'Rostro registrado exitosamente'
            }), 200
        else:
            return jsonify({'error': 'No se pudo registrar el rostro'}), 400
            
    except Exception as e:
        logger.error(f"❌ Error registrando rostro: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@faceid_bp.route('/recognize', methods=['POST'])
def recognize_face():
    """Reconoce un rostro para autenticación"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Imagen requerida'}), 400
        
        image_file = request.files['image']
        
        if image_file.filename == '':
            return jsonify({'error': 'Archivo no seleccionado'}), 400
        
        # Guardar imagen temporalmente
        image_path = os.path.join(UPLOAD_FOLDER, 'temp_face.jpg')
        image_file.save(image_path)
        
        # Reconocer rostro
        email = face_recognizer.recognize_face(image_path)
        
        # Limpiar archivo temporal
        try:
            os.remove(image_path)
        except:
            pass
        
        if email:
            # Configurar sesión
            session.permanent = True
            session['email'] = email
            session['auth_method'] = 'faceid'
            session['authenticated'] = True
            
            logger.info(f"✅ Autenticación Face ID exitosa: {email}")
            return jsonify({
                'success': True,
                'email': email,
                'message': 'Autenticación facial exitosa'
            }), 200
        else:
            return jsonify({'error': 'Rostro no reconocido'}), 401
            
    except Exception as e:
        logger.error(f"❌ Error reconociendo rostro: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@faceid_bp.route('/status', methods=['GET'])
@login_required
def faceid_status():
    """Obtiene el estado del Face ID para el usuario"""
    try:
        email = session.get('email')
        # En una implementación real, verificaríamos en la base de datos
        # si el usuario tiene rostro registrado
        
        return jsonify({
            'registered': face_recognizer.get_registered_faces_count() > 0,
            'message': 'Face ID disponible'
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error obteniendo estado Face ID: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@faceid_bp.route('/health', methods=['GET'])
def faceid_health():
    """Health check para servicio Face ID"""
    try:
        return jsonify({
            'status': 'OK',
            'service': 'Face ID',
            'faces_registered': face_recognizer.get_registered_faces_count(),
            'message': 'Servicio Face ID funcionando'
        }), 200
    except Exception as e:
        logger.error(f"❌ Error en health check Face ID: {e}")
        return jsonify({'status': 'ERROR', 'service': 'Face ID'}), 500