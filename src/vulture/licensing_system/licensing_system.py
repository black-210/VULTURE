"""Enterprise Licensing System"""
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import Dict, Optional, List
import logging

logger = logging.getLogger(__name__)

class LicenseManager:
    """Enterprise license management"""
    
    LICENSE_TYPES = ['trial', 'commercial', 'enterprise', 'academic']
    
    def __init__(self, db_path: str = 'licenses.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize license database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS licenses (
                id INTEGER PRIMARY KEY,
                license_key TEXT UNIQUE NOT NULL,
                organization TEXT NOT NULL,
                license_type TEXT NOT NULL,
                max_users INTEGER,
                issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expiry_date TIMESTAMP,
                features TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS usage_logs (
                id INTEGER PRIMARY KEY,
                license_key TEXT NOT NULL,
                user_id TEXT,
                action TEXT,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (license_key) REFERENCES licenses(license_key)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY,
                license_key TEXT NOT NULL,
                invoice_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                amount REAL,
                status TEXT DEFAULT 'pending',
                FOREIGN KEY (license_key) REFERENCES licenses(license_key)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_license_key(self, organization: str) -> str:
        """Generate unique license key"""
        import uuid
        key_base = f"{organization}{uuid.uuid4().hex}"
        license_key = hashlib.sha256(key_base.encode()).hexdigest()[:32].upper()
        return f"VULTURE-{license_key}"
    
    def create_license(self, organization: str, license_type: str, 
                      max_users: int, validity_days: int = 365,
                      features: List[str] = None) -> Optional[str]:
        """Create new license"""
        if license_type not in self.LICENSE_TYPES:
            return None
        
        if features is None:
            features = []
        
        license_key = self.generate_license_key(organization)
        expiry_date = datetime.now() + timedelta(days=validity_days)
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            import json
            features_json = json.dumps(features)
            
            cursor.execute('''
                INSERT INTO licenses (license_key, organization, license_type, max_users, expiry_date, features)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (license_key, organization, license_type, max_users, expiry_date, features_json))
            
            conn.commit()
            conn.close()
            
            logger.info(f"License created: {license_key} for {organization}")
            return license_key
        
        except Exception as e:
            logger.error(f"Error creating license: {e}")
            return None
    
    def validate_license(self, license_key: str) -> Dict:
        """Validate license"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return {'valid': False, 'reason': 'License not found'}
        
        license_data = dict(row)
        
        # Check if active
        if not license_data['is_active']:
            return {'valid': False, 'reason': 'License is inactive'}
        
        # Check expiry
        expiry_date = datetime.fromisoformat(license_data['expiry_date'])
        if datetime.now() > expiry_date:
            return {'valid': False, 'reason': 'License expired'}
        
        # Check user limit
        cursor = sqlite3.connect(self.db_path).cursor()
        cursor.execute('''
            SELECT COUNT(DISTINCT user_id) FROM usage_logs 
            WHERE license_key = ? AND timestamp > datetime('now', '-1 day')
        ''', (license_key,))
        active_users = cursor.fetchone()[0]
        cursor.close()
        
        if active_users > license_data['max_users']:
            return {'valid': False, 'reason': 'User limit exceeded'}
        
        import json
        features = json.loads(license_data['features']) if license_data['features'] else []
        
        return {
            'valid': True,
            'organization': license_data['organization'],
            'license_type': license_data['license_type'],
            'max_users': license_data['max_users'],
            'active_users': active_users,
            'expiry_date': license_data['expiry_date'],
            'features': features
        }
    
    def log_usage(self, license_key: str, user_id: str, action: str) -> bool:
        """Log license usage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO usage_logs (license_key, user_id, action)
                VALUES (?, ?, ?)
            ''', (license_key, user_id, action))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error logging usage: {e}")
            return False
    
    def generate_invoice(self, license_key: str, amount: float) -> bool:
        """Generate billing invoice"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO billing (license_key, amount)
                VALUES (?, ?)
            ''', (license_key, amount))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Invoice generated for {license_key}: ${amount}")
            return True
        except Exception as e:
            logger.error(f"Error generating invoice: {e}")
            return False
    
    def get_compliance_report(self, license_key: str) -> Dict:
        """Generate compliance and usage report"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Get license info
        cursor.execute('SELECT * FROM licenses WHERE license_key = ?', (license_key,))
        license_data = dict(cursor.fetchone())
        
        # Get usage stats
        cursor.execute('''
            SELECT COUNT(*) as total_actions, 
                   COUNT(DISTINCT user_id) as unique_users
            FROM usage_logs 
            WHERE license_key = ?
        ''', (license_key,))
        
        usage_stats = dict(cursor.fetchone())
        
        # Get billing info
        cursor.execute('''
            SELECT COUNT(*) as total_invoices,
                   SUM(amount) as total_revenue
            FROM billing 
            WHERE license_key = ?
        ''', (license_key,))
        
        billing_stats = dict(cursor.fetchone())
        
        conn.close()
        
        return {
            'license_key': license_key,
            'organization': license_data['organization'],
            'license_type': license_data['license_type'],
            'max_users': license_data['max_users'],
            'issue_date': license_data['issue_date'],
            'expiry_date': license_data['expiry_date'],
            'usage_stats': usage_stats,
            'billing_stats': billing_stats
        }
