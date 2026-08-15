"""Marketplace API"""
from typing import Dict, List, Optional
from .registry import PluginRegistry
from .validator import PluginValidator
from .installer import PluginInstaller
import logging

logger = logging.getLogger(__name__)

class MarketplaceAPI:
    """REST API for plugin marketplace"""
    
    def __init__(self, db_path: str = 'plugins_registry.db', plugin_dir: str = './plugins'):
        self.registry = PluginRegistry(db_path)
        self.installer = PluginInstaller(plugin_dir)
        self.validator = PluginValidator()
    
    def publish_plugin(self, manifest_path: str, plugin_path: str) -> Dict:
        """Publish plugin to marketplace"""
        # Validate manifest
        valid, errors = self.validator.validate_manifest(manifest_path)
        
        if not valid:
            return {
                'success': False,
                'errors': errors
            }
        
        # Validate code
        try:
            with open(plugin_path, 'r') as f:
                code = f.read()
            
            risks = self.validator.scan_security_risks(code)
            
            if risks:
                logger.warning(f"Security risks detected: {risks}")
        except:
            pass
        
        # Register plugin
        import json
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        
        success = self.registry.register_plugin(
            name=manifest['name'],
            version=manifest['version'],
            author=manifest.get('author', 'Unknown'),
            description=manifest.get('description', ''),
            repository=manifest.get('repository', '')
        )
        
        return {
            'success': success,
            'plugin_name': manifest['name'],
            'version': manifest['version']
        }
    
    def search(self, query: str) -> List[Dict]:
        """Search marketplace"""
        return self.registry.search_plugins(query)
    
    def get_plugin_info(self, plugin_name: str) -> Optional[Dict]:
        """Get plugin information"""
        return self.registry.get_plugin(plugin_name)
    
    def list_plugins(self, limit: int = 100) -> List[Dict]:
        """List all plugins"""
        return self.registry.list_plugins(limit)
    
    def install_plugin(self, plugin_name: str, url: str) -> Dict:
        """Install plugin"""
        success = self.installer.install_from_url(url, plugin_name)
        
        if success:
            self.registry.increment_downloads(plugin_name)
        
        return {
            'success': success,
            'plugin_name': plugin_name
        }
    
    def uninstall_plugin(self, plugin_name: str) -> Dict:
        """Uninstall plugin"""
        success = self.installer.uninstall(plugin_name)
        
        return {
            'success': success,
            'plugin_name': plugin_name
        }
    
    def rate_plugin(self, plugin_name: str, user_id: str, rating: int, review: str = '') -> Dict:
        """Rate plugin"""
        if rating < 1 or rating > 5:
            return {
                'success': False,
                'error': 'Rating must be between 1 and 5'
            }
        
        success = self.registry.update_rating(plugin_name, user_id, rating, review)
        
        return {
            'success': success,
            'plugin_name': plugin_name,
            'rating': rating
        }
