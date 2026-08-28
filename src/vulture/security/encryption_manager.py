"""
VULTURE Encryption Manager Module
==================================
Secure encryption, key management, and data protection system
with support for multiple encryption algorithms and secure storage.

Features:
    - AES encryption/decryption
    - Key derivation and management
    - Secure key storage
    - File encryption
    - Data signing and verification
    - Secure random number generation
"""

import os
import json
import hashlib
import hmac
from typing import Any, Dict, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
import logging
from datetime import datetime, timedelta

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False

logger = logging.getLogger(__name__)


@dataclass
class EncryptionKey:
    """Encryption key metadata"""
    key_id: str
    algorithm: str
    created_at: datetime
    expires_at: Optional[datetime] = None
    
    def is_expired(self) -> bool:
        """Check if key is expired"""
        if self.expires_at is None:
            return False
        return datetime.now() > self.expires_at


class KeyDerivation:
    """Key derivation functions"""
    
    @staticmethod
    def derive_key_pbkdf2(password: str, salt: Optional[bytes] = None,
                        iterations: int = 100000) -> Tuple[bytes, bytes]:
        """Derive key using PBKDF2"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        if salt is None:
            salt = os.urandom(16)
        
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode())
        return key, salt
    
    @staticmethod
    def derive_key_scrypt(password: str, salt: Optional[bytes] = None) -> Tuple[bytes, bytes]:
        """Derive key using Scrypt"""
        try:
            from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
        except ImportError:
            raise ImportError("cryptography library required")
        
        if salt is None:
            salt = os.urandom(16)
        
        kdf = Scrypt(
            salt=salt,
            length=32,
            n=2**14,
            r=8,
            p=1,
            backend=default_backend()
        )
        
        key = kdf.derive(password.encode())
        return key, salt


class EncryptionManager:
    """Central encryption management"""
    
    def __init__(self, key_directory: Optional[Path] = None):
        if not CRYPTO_AVAILABLE:
            logger.warning("cryptography library not available")
        
        self.key_directory = key_directory or Path.home() / '.vulture' / 'keys'
        self.key_directory.mkdir(parents=True, exist_ok=True)
        self.keys: Dict[str, Tuple[bytes, EncryptionKey]] = {}
    
    def generate_key(self, key_id: str, expires_in_days: Optional[int] = None) -> bytes:
        """Generate new encryption key"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        key = Fernet.generate_key()
        
        key_metadata = EncryptionKey(
            key_id=key_id,
            algorithm='Fernet',
            created_at=datetime.now(),
            expires_at=(datetime.now() + timedelta(days=expires_in_days))
            if expires_in_days else None
        )
        
        self.keys[key_id] = (key, key_metadata)
        self._save_key(key_id, key, key_metadata)
        
        logger.info(f"Generated encryption key: {key_id}")
        return key
    
    def _save_key(self, key_id: str, key: bytes, metadata: EncryptionKey) -> None:
        """Save key to secure storage"""
        key_file = self.key_directory / f"{key_id}.key"
        metadata_file = self.key_directory / f"{key_id}.meta"
        
        # Save key
        key_file.write_bytes(key)
        key_file.chmod(0o600)
        
        # Save metadata
        metadata_dict = {
            'key_id': metadata.key_id,
            'algorithm': metadata.algorithm,
            'created_at': metadata.created_at.isoformat(),
            'expires_at': metadata.expires_at.isoformat() if metadata.expires_at else None
        }
        metadata_file.write_text(json.dumps(metadata_dict))
    
    def load_key(self, key_id: str) -> Optional[bytes]:
        """Load key from storage"""
        if key_id in self.keys:
            key, metadata = self.keys[key_id]
            
            if metadata.is_expired():
                logger.warning(f"Key {key_id} has expired")
                return None
            
            return key
        
        key_file = self.key_directory / f"{key_id}.key"
        if key_file.exists():
            key = key_file.read_bytes()
            self.keys[key_id] = (key, EncryptionKey(
                key_id=key_id,
                algorithm='Fernet',
                created_at=datetime.now()
            ))
            return key
        
        logger.warning(f"Key not found: {key_id}")
        return None
    
    def encrypt_data(self, data: bytes, key_id: str) -> Optional[bytes]:
        """Encrypt data"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        key = self.load_key(key_id)
        if key is None:
            return None
        
        try:
            cipher = Fernet(key)
            encrypted = cipher.encrypt(data)
            return encrypted
        except Exception as e:
            logger.error(f"Encryption error: {e}")
            return None
    
    def decrypt_data(self, encrypted_data: bytes, key_id: str) -> Optional[bytes]:
        """Decrypt data"""
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library required")
        
        key = self.load_key(key_id)
        if key is None:
            return None
        
        try:
            cipher = Fernet(key)
            decrypted = cipher.decrypt(encrypted_data)
            return decrypted
        except Exception as e:
            logger.error(f"Decryption error: {e}")
            return None
    
    def encrypt_file(self, input_path: Path, output_path: Path, key_id: str) -> bool:
        """Encrypt file"""
        try:
            data = input_path.read_bytes()
            encrypted = self.encrypt_data(data, key_id)
            
            if encrypted is None:
                return False
            
            output_path.write_bytes(encrypted)
            output_path.chmod(0o600)
            return True
        except Exception as e:
            logger.error(f"File encryption error: {e}")
            return False
    
    def decrypt_file(self, input_path: Path, output_path: Path, key_id: str) -> bool:
        """Decrypt file"""
        try:
            encrypted = input_path.read_bytes()
            decrypted = self.decrypt_data(encrypted, key_id)
            
            if decrypted is None:
                return False
            
            output_path.write_bytes(decrypted)
            return True
        except Exception as e:
            logger.error(f"File decryption error: {e}")
            return False


class SignatureManager:
    """Digital signatures for data integrity"""
    
    @staticmethod
    def sign_data(data: bytes, key: bytes, algorithm: str = 'sha256') -> bytes:
        """Sign data with HMAC"""
        if algorithm == 'sha256':
            return hmac.new(key, data, hashlib.sha256).digest()
        elif algorithm == 'sha512':
            return hmac.new(key, data, hashlib.sha512).digest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def verify_signature(data: bytes, signature: bytes, key: bytes,
                        algorithm: str = 'sha256') -> bool:
        """Verify HMAC signature"""
        expected_signature = SignatureManager.sign_data(data, key, algorithm)
        return hmac.compare_digest(signature, expected_signature)
    
    @staticmethod
    def hash_data(data: bytes, algorithm: str = 'sha256') -> str:
        """Hash data"""
        if algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")


class SecureStorage:
    """Secure storage for sensitive data"""
    
    def __init__(self, storage_path: Path, encryption_manager: EncryptionManager):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self.encryption_manager = encryption_manager
    
    def store_secret(self, name: str, value: str, key_id: str) -> bool:
        """Store encrypted secret"""
        try:
            encrypted = self.encryption_manager.encrypt_data(
                value.encode(), key_id
            )
            
            if encrypted is None:
                return False
            
            secret_file = self.storage_path / f"{name}.secret"
            secret_file.write_bytes(encrypted)
            secret_file.chmod(0o600)
            return True
        except Exception as e:
            logger.error(f"Secret storage error: {e}")
            return False
    
    def retrieve_secret(self, name: str, key_id: str) -> Optional[str]:
        """Retrieve encrypted secret"""
        try:
            secret_file = self.storage_path / f"{name}.secret"
            if not secret_file.exists():
                return None
            
            encrypted = secret_file.read_bytes()
            decrypted = self.encryption_manager.decrypt_data(encrypted, key_id)
            
            if decrypted is None:
                return None
            
            return decrypted.decode()
        except Exception as e:
            logger.error(f"Secret retrieval error: {e}")
            return None


# Global instance
_encryption_manager = EncryptionManager() if CRYPTO_AVAILABLE else None


def get_encryption_manager() -> Optional[EncryptionManager]:
    """Get global encryption manager"""
    return _encryption_manager
