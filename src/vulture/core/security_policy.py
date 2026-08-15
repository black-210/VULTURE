"""RBAC, HMAC signing, audit logging, sandboxed execution."""

import hmac
import hashlib
import json
from datetime import datetime
from typing import Set, Dict, Any, Callable
from enum import Enum
import logging
import threading

logger = logging.getLogger(__name__)


class Role(Enum):
    """User roles for RBAC."""
    USER = "user"
    ANALYST = "analyst"
    RESEARCHER = "researcher"
    ADMIN = "admin"


class Permission(Enum):
    """Fine-grained permissions."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    ADMIN = "admin"


class RBAC:
    """Role-Based Access Control."""

    ROLE_PERMISSIONS = {
        Role.USER: {Permission.READ},
        Role.ANALYST: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
        Role.RESEARCHER: {Permission.READ, Permission.WRITE, Permission.EXECUTE},
        Role.ADMIN: {Permission.READ, Permission.WRITE, Permission.EXECUTE, Permission.DELETE, Permission.ADMIN},
    }

    def __init__(self, role: Role = Role.USER):
        self.role = role
        self.permissions = self.ROLE_PERMISSIONS.get(role, set())

    def has_permission(self, permission: Permission) -> bool:
        """Check if user has permission.
        
        Args:
            permission: Permission to check
            
        Returns:
            True if permission granted
        """
        return permission in self.permissions

    def require_permission(self, permission: Permission) -> None:
        """Require permission, raise if not granted.
        
        Args:
            permission: Required permission
        """
        if not self.has_permission(permission):
            raise PermissionError(f"{self.role.value} not authorized for {permission.value}")


class SecurityPolicy:
    """Security: HMAC signing, audit logging."""

    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or "default-insecure-key"
        self.audit_log: list = []
        self._lock = threading.RLock()

    def sign(self, data: str) -> str:
        """Create HMAC signature.
        
        Args:
            data: Data to sign
            
        Returns:
            Hex digest signature
        """
        return hmac.new(
            self.secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()

    def verify(self, data: str, signature: str) -> bool:
        """Verify HMAC signature.
        
        Args:
            data: Original data
            signature: Signature to verify
            
        Returns:
            True if valid
        """
        expected = self.sign(data)
        return hmac.compare_digest(expected, signature)

    def audit_log_event(self, event_type: str, user: str, action: str, resource: str, 
                        result: str = "success", details: Dict[str, Any] = None) -> None:
        """Log security event.
        
        Args:
            event_type: Type of event
            user: User ID
            action: Action performed
            resource: Resource accessed
            result: success/failure
            details: Additional details
        """
        with self._lock:
            event = {
                "timestamp": datetime.utcnow().isoformat(),
                "event_type": event_type,
                "user": user,
                "action": action,
                "resource": resource,
                "result": result,
                "details": details or {}
            }
            self.audit_log.append(event)
            logger.info(f"[AUDIT] {user} {action} {resource} -> {result}")

    def get_audit_log(self) -> list:
        """Get audit log.
        
        Returns:
            List of audit events
        """
        with self._lock:
            return list(self.audit_log)

    def export_audit_log(self, path: str) -> None:
        """Export audit log to JSON.
        
        Args:
            path: Output file path
        """
        with self._lock:
            with open(path, 'w') as f:
                json.dump(self.audit_log, f, indent=2)
            logger.info(f"✓ Exported audit log to: {path}")
