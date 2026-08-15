"""Plugin Installer"""
import os
import shutil
import zipfile
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class PluginInstaller:
    """Install and manage plugins"""
    
    def __init__(self, plugin_dir: str = './plugins'):
        self.plugin_dir = Path(plugin_dir)
        self.plugin_dir.mkdir(parents=True, exist_ok=True)
    
    def install_from_file(self, plugin_path: str, plugin_name: str) -> bool:
        """Install plugin from local file"""
        try:
            plugin_file = Path(plugin_path)
            
            if not plugin_file.exists():
                logger.error(f"Plugin file not found: {plugin_path}")
                return False
            
            # Create plugin directory
            target_dir = self.plugin_dir / plugin_name
            target_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract if zip
            if plugin_file.suffix == '.zip':
                with zipfile.ZipFile(plugin_file, 'r') as zip_ref:
                    zip_ref.extractall(target_dir)
            else:
                # Copy single file
                shutil.copy2(plugin_file, target_dir / plugin_file.name)
            
            logger.info(f"Plugin installed: {plugin_name} at {target_dir}")
            return True
        
        except Exception as e:
            logger.error(f"Installation failed: {e}")
            return False
    
    def install_from_url(self, url: str, plugin_name: str) -> bool:
        """Install plugin from remote URL"""
        try:
            import urllib.request
            
            target_file = self.plugin_dir / f"{plugin_name}.zip"
            
            logger.info(f"Downloading plugin from {url}")
            urllib.request.urlretrieve(url, target_file)
            
            # Install from file
            success = self.install_from_file(str(target_file), plugin_name)
            
            # Clean up download
            target_file.unlink()
            
            return success
        
        except Exception as e:
            logger.error(f"Download failed: {e}")
            return False
    
    def uninstall(self, plugin_name: str) -> bool:
        """Uninstall plugin"""
        try:
            plugin_path = self.plugin_dir / plugin_name
            
            if plugin_path.exists():
                shutil.rmtree(plugin_path)
                logger.info(f"Plugin uninstalled: {plugin_name}")
                return True
            else:
                logger.warning(f"Plugin not found: {plugin_name}")
                return False
        
        except Exception as e:
            logger.error(f"Uninstallation failed: {e}")
            return False
    
    def list_installed(self) -> list:
        """List all installed plugins"""
        if not self.plugin_dir.exists():
            return []
        
        return [d.name for d in self.plugin_dir.iterdir() if d.is_dir()]
    
    def get_plugin_info(self, plugin_name: str) -> Optional[dict]:
        """Get installed plugin information"""
        try:
            manifest_path = self.plugin_dir / plugin_name / 'manifest.json'
            
            if not manifest_path.exists():
                return None
            
            import json
            with open(manifest_path, 'r') as f:
                manifest = json.load(f)
            
            return manifest
        
        except Exception as e:
            logger.error(f"Error reading plugin info: {e}")
            return None
    
    def enable_plugin(self, plugin_name: str) -> bool:
        """Enable plugin by creating marker file"""
        try:
            marker_path = self.plugin_dir / plugin_name / '.enabled'
            marker_path.touch()
            logger.info(f"Plugin enabled: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to enable plugin: {e}")
            return False
    
    def disable_plugin(self, plugin_name: str) -> bool:
        """Disable plugin by removing marker file"""
        try:
            marker_path = self.plugin_dir / plugin_name / '.enabled'
            if marker_path.exists():
                marker_path.unlink()
            logger.info(f"Plugin disabled: {plugin_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to disable plugin: {e}")
            return False
    
    def is_plugin_enabled(self, plugin_name: str) -> bool:
        """Check if plugin is enabled"""
        marker_path = self.plugin_dir / plugin_name / '.enabled'
        return marker_path.exists()
