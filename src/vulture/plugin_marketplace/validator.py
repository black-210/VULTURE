"""Plugin Validator"""
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)

class PluginValidator:
    """Validate plugin integrity and security"""
    
    REQUIRED_FIELDS = ['name', 'version', 'author', 'entry_point']
    FORBIDDEN_IMPORTS = ['os.system', '__import__', 'eval', 'exec']
    
    @staticmethod
    def validate_manifest(manifest_path: str) -> Tuple[bool, List[str]]:
        """Validate plugin manifest file"""
        errors = []
        
        try:
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
        except FileNotFoundError:
            return False, ["Manifest file not found"]
        except json.JSONDecodeError:
            return False, ["Invalid JSON in manifest"]
        
        # Check required fields
        for field in PluginValidator.REQUIRED_FIELDS:
            if field not in manifest:
                errors.append(f"Missing required field: {field}")
        
        # Validate version format
        if 'version' in manifest:
            if not PluginValidator._is_valid_version(manifest['version']):
                errors.append("Invalid version format (use semantic versioning)")
        
        # Validate entry point
        if 'entry_point' in manifest:
            entry = manifest['entry_point']
            if not isinstance(entry, str) or ':' not in entry:
                errors.append("Entry point must be in format 'module:class'")
        
        return len(errors) == 0, errors
    
    @staticmethod
    def _is_valid_version(version: str) -> bool:
        """Check semantic versioning"""
        parts = version.split('.')
        if len(parts) != 3:
            return False
        try:
            for part in parts:
                int(part)
            return True
        except ValueError:
            return False
    
    @staticmethod
    def scan_security_risks(plugin_code: str) -> List[str]:
        """Scan plugin code for security risks"""
        risks = []
        
        for forbidden in PluginValidator.FORBIDDEN_IMPORTS:
            if forbidden in plugin_code:
                risks.append(f"Forbidden operation detected: {forbidden}")
        
        # Check for hardcoded credentials
        if 'password' in plugin_code.lower() and '=' in plugin_code:
            risks.append("Potential hardcoded credentials detected")
        
        # Check for unsafe file operations
        if 'open(' in plugin_code and 'eval' in plugin_code:
            risks.append("Potentially unsafe file operations")
        
        return risks
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
        """Calculate file hash for integrity verification"""
        hasher = hashlib.new(algorithm)
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    @staticmethod
    def validate_dependencies(requirements: List[str]) -> Tuple[bool, List[str]]:
        """Validate plugin dependencies"""
        errors = []
        
        try:
            import pkg_resources
            
            for req in requirements:
                try:
                    pkg_resources.require(req)
                except pkg_resources.DistributionNotFound:
                    errors.append(f"Dependency not installed: {req}")
                except pkg_resources.VersionConflict:
                    errors.append(f"Version conflict: {req}")
        except ImportError:
            logger.warning("pkg_resources not available for dependency checking")
        
        return len(errors) == 0, errors
