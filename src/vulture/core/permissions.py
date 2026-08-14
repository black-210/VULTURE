"""Permission Management System."""

from enum import Enum
from typing import Set, Dict
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


class Permission(Enum):
    """Permission types."""
    # File permissions
    FILE_READ = "file:read"
    FILE_WRITE = "file:write"
    FILE_DELETE = "file:delete"
    
    # Network permissions
    NETWORK_READ = "network:read"
    NETWORK_WRITE = "network:write"
    
    # Plugin permissions
    PLUGIN_LOAD = "plugin:load"
    PLUGIN_EXECUTE = "plugin:execute"
    
    # AI permissions
    AI_EXECUTE = "ai:execute"
    AI_INTERNET_SEARCH = "ai:internet_search"
    AI_CODE_GENERATION = "ai:code_generation"
    
    # System permissions
    SYSTEM_TERMINAL = "system:terminal"
    SYSTEM_PYTHON_EVAL = "system:python_eval"
    
    # Model permissions
    MODEL_DOWNLOAD = "model:download"
    MODEL_EXECUTE = "model:execute"


@dataclass
class Role:
    """User role with permissions."""
    name: str
    permissions: Set[Permission] = field(default_factory=set)
    description: str = ""


class PermissionManager:
    """Manage permissions and access control."""
    
    def __init__(self):
        """Initialize permission manager."""
        self.roles: Dict[str, Role] = {}
        self.user_roles: Dict[str, Set[str]] = {}
        self._create_default_roles()
    
    def _create_default_roles(self) -> None:
        """Create default roles."""
        # Admin role - all permissions
        admin_perms = set(Permission)
        self.roles["admin"] = Role("admin", admin_perms, "Administrator role")
        
        # User role - safe operations
        user_perms = {
            Permission.FILE_READ,
            Permission.NETWORK_READ,
            Permission.AI_EXECUTE,
            Permission.MODEL_EXECUTE,
        }
        self.roles["user"] = Role("user", user_perms, "Regular user role")
        
        # Guest role - read-only
        guest_perms = {
            Permission.FILE_READ,
            Permission.NETWORK_READ,
        }
        self.roles["guest"] = Role("guest", guest_perms, "Guest read-only role")
    
    def grant_permission(self, user: str, permission: Permission) -> None:
        """Grant permission to user.
        
        Args:
            user: User identifier
            permission: Permission to grant
        """
        if user not in self.user_roles:
            self.user_roles[user] = set()
        # Implement user-specific permissions
        logger.debug(f"Granted {permission} to {user}")
    
    def has_permission(self, user: str, permission: Permission) -> bool:
        """Check if user has permission.
        
        Args:
            user: User identifier
            permission: Permission to check
        
        Returns:
            True if user has permission
        """
        # Check role permissions (default to 'user' role)
        user_roles = self.user_roles.get(user, {"user"})
        for role_name in user_roles:
            if role_name in self.roles:
                if permission in self.roles[role_name].permissions:
                    return True
        return False
    
    def check_permission(self, user: str, permission: Permission) -> None:
        """Check permission or raise exception.
        
        Args:
            user: User identifier
            permission: Permission to check
        
        Raises:
            PermissionError: If user lacks permission
        """
        if not self.has_permission(user, permission):
            raise PermissionError(f"User {user} lacks permission: {permission}")
    
    def assign_role(self, user: str, role: str) -> None:
        """Assign role to user.
        
        Args:
            user: User identifier
            role: Role name
        """
        if role not in self.roles:
            raise ValueError(f"Unknown role: {role}")
        
        if user not in self.user_roles:
            self.user_roles[user] = set()
        
        self.user_roles[user].add(role)
        logger.info(f"Assigned role {role} to {user}")
