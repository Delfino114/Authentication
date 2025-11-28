import face_recognition
import numpy as np
import logging

logger = logging.getLogger(__name__)

class FaceRecognizer:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_emails = []
    
    def register_face(self, image_path: str, email: str) -> bool:
        """Registra un rostro para un usuario"""
        try:
            # Cargar y codificar la imagen
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                logger.warning("No se detectó ningún rostro en la imagen")
                return False
            
            # Usar la primera codificación de rostro encontrada
            face_encoding = face_encodings[0]
            
            # Guardar la codificación
            self.known_face_encodings.append(face_encoding)
            self.known_face_emails.append(email)
            
            logger.info(f"✅ Rostro registrado para: {email}")
            return True
            
        except Exception as e:
            logger.error(f"❌ Error registrando rostro: {e}")
            return False
    
    def recognize_face(self, image_path: str) -> str:
        """Reconoce un rostro y devuelve el email asociado"""
        try:
            # Cargar y codificar la imagen
            image = face_recognition.load_image_file(image_path)
            face_encodings = face_recognition.face_encodings(image)
            
            if len(face_encodings) == 0:
                logger.warning("No se detectó ningún rostro en la imagen")
                return None
            
            face_encoding = face_encodings[0]
            
            # Comparar con rostros conocidos
            matches = face_recognition.compare_faces(
                self.known_face_encodings, 
                face_encoding
            )
            
            face_distances = face_recognition.face_distance(
                self.known_face_encodings, 
                face_encoding
            )
            
            # Encontrar la mejor coincidencia
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                email = self.known_face_emails[best_match_index]
                logger.info(f"✅ Rostro reconocido: {email}")
                return email
            
            logger.warning("❌ Rostro no reconocido")
            return None
            
        except Exception as e:
            logger.error(f"❌ Error reconociendo rostro: {e}")
            return None
    
    def get_registered_faces_count(self) -> int:
        """Devuelve el número de rostros registrados"""
        return len(self.known_face_emails)