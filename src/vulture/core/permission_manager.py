"""Role-Based Access Control (RBAC)

Manages user roles and permissions.
"""

from enum import Enum
from typing import Set, Dict
import logging


class Role(Enum):
    """User roles"""
    USER = "user"              # Read-only access
    ANALYST = "analyst"        # Data analysis, inference
    RESEARCHER = "researcher"  # Full framework access
    ADMIN = "admin"            # System configuration, plugins


class PermissionManager:
    """Permission management system"""
    
    ROLE_PERMISSIONS: Dict[Role, Set[str]] = {
        Role.USER: {"read", "info"},
        Role.ANALYST: {"read", "analyze", "inference", "info"},
        Role.RESEARCHER: {"read", "write", "analyze", "inference", "framework", "info"},
        Role.ADMIN: {"read", "write", "delete", "analyze", "inference", "framework", "admin", "info"},
    }
    
    def __init__(self):
        self.user_roles: Dict[str, Role] = {}
        self.logger = logging.getLogger("vulture.permissions")
    
    def set_user_role(self, user_id: str, role: Role) -> None:
        """Set user role"""
        self.user_roles[user_id] = role
        self.logger.info(f"Set {user_id} role to {role.value}")
    
    def has_permission(self, user_id: str, permission: str) -> bool:
        """Check if user has permission"""
        role = self.user_roles.get(user_id, Role.USER)
        return permission in self.ROLE_PERMISSIONS[role]
    
    def get_user_role(self, user_id: str) -> Role:
        """Get user role"""
        return self.user_roles.get(user_id, Role.USER)
    
    def get_user_permissions(self, user_id: str) -> Set[str]:
        """Get all permissions for user"""
        role = self.get_user_role(user_id)
        return self.ROLE_PERMISSIONS[role].copy()
