from datetime import datetime
from typing import Optional, Dict, Any

class User:
    def __init__(self, email: str, password: str, first_name: str, last_name: str, 
                 auth_method: str = 'totp', phone_number: Optional[str] = None):
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.auth_method = auth_method
        self.phone_number = phone_number
        self.verified = False
        self.secret = None
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'auth_method': self.auth_method,
            'phone_number': self.phone_number,
            'verified': self.verified,
            'secret': self.secret,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'User':
        user = cls(
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            auth_method=data.get('auth_method', 'totp'),
            phone_number=data.get('phone_number')
        )
        user.verified = data.get('verified', False)
        user.secret = data.get('secret')
        user.created_at = data.get('created_at', datetime.now())
        user.updated_at = data.get('updated_at', datetime.now())
        return user

class OTPRecord:
    def __init__(self, phone_number: str, otp: str, expires_at: datetime):
        self.phone_number = phone_number
        self.otp = otp
        self.expires_at = expires_at
        self.used = False
        self.created_at = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'phone_number': self.phone_number,
            'otp': self.otp,
            'expires_at': self.expires_at,
            'used': self.used,
            'created_at': self.created_at
        }
    
    def is_expired(self) -> bool:
        return datetime.now() > self.expires_at