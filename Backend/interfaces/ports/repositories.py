from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class UserRepositoryPort(ABC):
    @abstractmethod
    def save_user(self, email: str, user_data: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def update_user(self, email: str, updates: Dict[str, Any]) -> bool:
        pass
    
    @abstractmethod
    def user_exists(self, email: str) -> bool:
        pass
    
    @abstractmethod
    def get_user_secret(self, email: str) -> Optional[str]:
        pass
    
    @abstractmethod
    def set_user_secret(self, email: str, secret: str) -> bool:
        pass

class OTPRepositoryPort(ABC):
    @abstractmethod
    def save_otp(self, phone_number: str, otp: str, expires_at) -> bool:
        pass
    
    @abstractmethod
    def get_otp(self, phone_number: str) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    def mark_otp_used(self, phone_number: str) -> bool:
        pass