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