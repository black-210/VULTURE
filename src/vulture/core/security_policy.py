"""Security Policy - Permission controls and security enforcement."""

from typing import Dict, Set, Optional, List
from enum import Enum
from datetime import datetime
import logging
import hashlib
import hmac

logger = logging.getLogger(__name__)


class Permission(Enum):
    """Available permissions."""
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    DELETE = "delete"
    NETWORK = "network"
    FILESYSTEM = "filesystem"
    GPU = "gpu"
    ADMIN = "admin"


class Role(Enum):
    """Available roles."""
    USER = "user"
    ANALYST = "analyst"
    RESEARCHER = "researcher"
    ADMIN = "admin"


class SecurityPolicy:
    """Manage security policies, permissions, and access control."""
    
    def __init__(self):
        self._roles: Dict[Role, Set[Permission]] = self._initialize_roles()
        self._users: Dict[str, Role] = {}
        self._audit_log: List[Dict] = []
        self._secret_key: Optional[str] = None
        logger.info("SecurityPolicy initialized")
    
    @staticmethod
    def _initialize_roles() -> Dict[Role, Set[Permission]]:
        """Initialize default role-permission mapping."""
        return {
            Role.USER: {Permission.READ, Permission.EXECUTE},
            Role.ANALYST: {
                Permission.READ, Permission.WRITE, Permission.EXECUTE,
                Permission.FILESYSTEM
            },
            Role.RESEARCHER: {
                Permission.READ, Permission.WRITE, Permission.EXECUTE,
                Permission.FILESYSTEM, Permission.NETWORK, Permission.GPU
            },
            Role.ADMIN: {
                Permission.READ, Permission.WRITE, Permission.EXECUTE,
                Permission.DELETE, Permission.NETWORK, Permission.FILESYSTEM,
                Permission.GPU, Permission.ADMIN
            },
        }
    
    def add_user(self, username: str, role: Role) -> bool:
        """Add user with role."""
        if username in self._users:
            logger.warning(f"User {username} already exists")
            return False
        
        self._users[username] = role
        self._log_audit(f"User '{username}' added with role '{role.value}'")
        logger.info(f"User added: {username} ({role.value})")
        return True
    
    def remove_user(self, username: str) -> bool:
        """Remove user."""
        if username not in self._users:
            return False
        
        del self._users[username]
        self._log_audit(f"User '{username}' removed")
        logger.info(f"User removed: {username}")
        return True
    
    def set_user_role(self, username: str, role: Role) -> bool:
        """Set user role."""
        if username not in self._users:
            return False
        
        old_role = self._users[username]
        self._users[username] = role
        self._log_audit(f"User '{username}' role changed from '{old_role.value}' to '{role.value}'")
        logger.info(f"User {username} role changed to {role.value}")
        return True
    
    def get_user_role(self, username: str) -> Optional[Role]:
        """Get user role."""
        return self._users.get(username)
    
    def get_user_permissions(self, username: str) -> Set[Permission]:
        """Get permissions for user."""
        role = self._users.get(username)
        if role is None:
            return set()
        return self._roles.get(role, set()).copy()
    
    def has_permission(self, username: str, permission: Permission) -> bool:
        """Check if user has permission."""
        permissions = self.get_user_permissions(username)
        return permission in permissions
    
    def grant_role_permission(self, role: Role, permission: Permission) -> bool:
        """Grant additional permission to role."""
        if permission in self._roles[role]:
            return False
        
        self._roles[role].add(permission)
        self._log_audit(f"Permission '{permission.value}' granted to role '{role.value}'")
        logger.info(f"Permission {permission.value} granted to role {role.value}")
        return True
    
    def revoke_role_permission(self, role: Role, permission: Permission) -> bool:
        """Revoke permission from role."""
        if permission not in self._roles[role]:
            return False
        
        self._roles[role].discard(permission)
        self._log_audit(f"Permission '{permission.value}' revoked from role '{role.value}'")
        logger.info(f"Permission {permission.value} revoked from role {role.value}")
        return True
    
    def set_secret_key(self, key: str) -> None:
        """Set secret key for HMAC signing."""
        self._secret_key = key
        logger.debug("Secret key set")
    
    def sign_data(self, data: str) -> Optional[str]:
        """Sign data with secret key."""
        if not self._secret_key:
            return None
        
        return hmac.new(
            self._secret_key.encode(),
            data.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def verify_signature(self, data: str, signature: str) -> bool:
        """Verify data signature."""
        if not self._secret_key:
            return False
        
        expected = self.sign_data(data)
        return expected == signature if expected else False
    
    def _log_audit(self, message: str) -> None:
        """Log audit entry."""
        self._audit_log.append({
            'timestamp': datetime.now().isoformat(),
            'message': message,
        })
    
    def get_audit_log(self, limit: Optional[int] = None) -> List[Dict]:
        """Get audit log entries."""
        if limit:
            return self._audit_log[-limit:]
        return self._audit_log.copy()
    
    def clear_audit_log(self) -> None:
        """Clear audit log."""
        self._audit_log.clear()
        logger.info("Audit log cleared")
    
    def get_summary(self) -> Dict[str, any]:
        """Get security policy summary."""
        return {
            'total_users': len(self._users),
            'total_roles': len(self._roles),
            'audit_log_entries': len(self._audit_log),
            'has_secret_key': self._secret_key is not None,
            'users': list(self._users.keys()),
        }