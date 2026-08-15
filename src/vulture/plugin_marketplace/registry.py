"""Plugin Registry Database"""
import json
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class PluginRegistry:
    """Central registry for plugins"""
    
    def __init__(self, db_path: str = 'plugins_registry.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize plugin registry database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create plugins table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plugins (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                version TEXT NOT NULL,
                author TEXT NOT NULL,
                description TEXT,
                repository TEXT,
                downloads INTEGER DEFAULT 0,
                rating REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create versions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY,
                plugin_id INTEGER NOT NULL,
                version TEXT NOT NULL,
                release_notes TEXT,
                release_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                download_url TEXT,
                file_hash TEXT,
                FOREIGN KEY (plugin_id) REFERENCES plugins(id)
            )
        ''')
        
        # Create ratings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY,
                plugin_id INTEGER NOT NULL,
                user_id TEXT NOT NULL,
                rating INTEGER,
                review TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (plugin_id) REFERENCES plugins(id)
            )
        ''')
        
        conn.commit()
        conn.close()
        logger.info(f"Plugin registry initialized at {self.db_path}")
    
    def register_plugin(self, name: str, version: str, author: str, 
                       description: str, repository: str) -> bool:
        """Register a new plugin"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO plugins (name, version, author, description, repository)
                VALUES (?, ?, ?, ?, ?)
            ''', (name, version, author, description, repository))
            
            plugin_id = cursor.lastrowid
            
            # Add initial version
            cursor.execute('''
                INSERT INTO versions (plugin_id, version)
                VALUES (?, ?)
            ''', (plugin_id, version))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Plugin registered: {name} v{version}")
            return True
        except sqlite3.IntegrityError:
            logger.error(f"Plugin already exists: {name}")
            return False
    
    def get_plugin(self, name: str) -> Optional[Dict]:
        """Get plugin details"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM plugins WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def list_plugins(self, limit: int = 100) -> List[Dict]:
        """List all plugins"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM plugins ORDER BY rating DESC LIMIT ?', (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def update_rating(self, plugin_name: str, user_id: str, rating: int, review: str = '') -> bool:
        """Update plugin rating"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get plugin ID
            cursor.execute('SELECT id FROM plugins WHERE name = ?', (plugin_name,))
            result = cursor.fetchone()
            
            if not result:
                return False
            
            plugin_id = result[0]
            
            # Insert or update rating
            cursor.execute('''
                INSERT OR REPLACE INTO ratings (plugin_id, user_id, rating, review)
                VALUES (?, ?, ?, ?)
            ''', (plugin_id, user_id, rating, review))
            
            # Update average rating
            cursor.execute('''
                UPDATE plugins 
                SET rating = (SELECT AVG(rating) FROM ratings WHERE plugin_id = ?)
                WHERE id = ?
            ''', (plugin_id, plugin_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error updating rating: {e}")
            return False
    
    def increment_downloads(self, plugin_name: str) -> bool:
        """Increment download count"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE plugins 
                SET downloads = downloads + 1,
                    updated_at = CURRENT_TIMESTAMP
                WHERE name = ?
            ''', (plugin_name,))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error incrementing downloads: {e}")
            return False
    
    def search_plugins(self, query: str) -> List[Dict]:
        """Search plugins by name or description"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM plugins 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY rating DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
