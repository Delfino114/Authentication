# Ruta: Backend/interfaces/ports/external_services.py
from abc import ABC, abstractmethod

class SMSServicePort(ABC):
    @abstractmethod
    def send_otp(self, phone_number: str, otp: str) -> bool:
        pass

class QRServicePort(ABC):
    @abstractmethod
    def generate_qr_image(self, uri: str) -> bytes:
        pass

class FaceRecognitionPort(ABC):
    @abstractmethod
    def register_face(self, image_path: str, user_id: str) -> bool:
        pass
    
    @abstractmethod
    def recognize_face(self, image_path: str) -> str:
        pass