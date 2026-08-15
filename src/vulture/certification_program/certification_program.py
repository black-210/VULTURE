"""Certification Program System"""
import sqlite3
import hashlib
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CertificationProgram:
    """Manage certification courses and exams"""
    
    def __init__(self, db_path: str = 'certifications.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize certification database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS courses (
                id INTEGER PRIMARY KEY,
                course_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT,
                level TEXT,
                duration_hours INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS modules (
                id INTEGER PRIMARY KEY,
                module_id TEXT UNIQUE NOT NULL,
                course_id TEXT NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                order_index INTEGER,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessments (
                id INTEGER PRIMARY KEY,
                assessment_id TEXT UNIQUE NOT NULL,
                module_id TEXT NOT NULL,
                title TEXT NOT NULL,
                questions TEXT,
                passing_score INTEGER DEFAULT 70,
                FOREIGN KEY (module_id) REFERENCES modules(module_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS enrollments (
                id INTEGER PRIMARY KEY,
                enrollment_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                enrolled_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                FOREIGN KEY (course_id) REFERENCES courses(course_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS assessment_results (
                id INTEGER PRIMARY KEY,
                result_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                assessment_id TEXT NOT NULL,
                score INTEGER,
                passed BOOLEAN,
                taken_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY,
                certificate_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                course_id TEXT NOT NULL,
                issued_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP,
                verification_hash TEXT UNIQUE
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_course(self, name: str, description: str, level: str, 
                     duration_hours: int) -> str:
        """Create new course"""
        import uuid
        course_id = f"COURSE-{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO courses (course_id, name, description, level, duration_hours)
            VALUES (?, ?, ?, ?, ?)
        ''', (course_id, name, description, level, duration_hours))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Course created: {course_id}")
        return course_id
    
    def add_module(self, course_id: str, title: str, content: str, 
                  order_index: int) -> str:
        """Add module to course"""
        import uuid
        module_id = f"MODULE-{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO modules (module_id, course_id, title, content, order_index)
            VALUES (?, ?, ?, ?, ?)
        ''', (module_id, course_id, title, content, order_index))
        
        conn.commit()
        conn.close()
        
        return module_id
    
    def enroll_user(self, user_id: str, course_id: str) -> str:
        """Enroll user in course"""
        import uuid
        enrollment_id = f"ENROLL-{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO enrollments (enrollment_id, user_id, course_id)
            VALUES (?, ?, ?)
        ''', (enrollment_id, user_id, course_id))
        
        conn.commit()
        conn.close()
        
        logger.info(f"User {user_id} enrolled in {course_id}")
        return enrollment_id
    
    def submit_assessment(self, user_id: str, assessment_id: str, 
                         score: int) -> bool:
        """Submit assessment result"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get passing score
            cursor.execute('SELECT passing_score FROM assessments WHERE assessment_id = ?', 
                          (assessment_id,))
            result = cursor.fetchone()
            
            if not result:
                return False
            
            passing_score = result[0]
            passed = score >= passing_score
            
            import uuid
            result_id = f"RESULT-{uuid.uuid4().hex[:8].upper()}"
            
            cursor.execute('''
                INSERT INTO assessment_results (result_id, user_id, assessment_id, score, passed)
                VALUES (?, ?, ?, ?, ?)
            ''', (result_id, user_id, assessment_id, score, passed))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error submitting assessment: {e}")
            return False
    
    def issue_certificate(self, user_id: str, course_id: str, 
                         validity_days: int = 365) -> Optional[str]:
        """Issue certificate to user"""
        try:
            import uuid
            certificate_id = f"CERT-{uuid.uuid4().hex[:8].upper()}"
            
            # Generate verification hash
            hash_input = f"{user_id}{course_id}{datetime.now()}"
            verification_hash = hashlib.sha256(hash_input.encode()).hexdigest()
            
            expires_at = datetime.now() + timedelta(days=validity_days)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO certificates (certificate_id, user_id, course_id, expires_at, verification_hash)
                VALUES (?, ?, ?, ?, ?)
            ''', (certificate_id, user_id, course_id, expires_at, verification_hash))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Certificate issued: {certificate_id}")
            return certificate_id
        
        except Exception as e:
            logger.error(f"Error issuing certificate: {e}")
            return None
    
    def verify_certificate(self, certificate_id: str) -> Optional[Dict]:
        """Verify certificate authenticity"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM certificates WHERE certificate_id = ?
        ''', (certificate_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        cert = dict(row)
        expires_at = datetime.fromisoformat(cert['expires_at'])
        is_valid = datetime.now() < expires_at
        
        return {
            'certificate_id': cert['certificate_id'],
            'user_id': cert['user_id'],
            'course_id': cert['course_id'],
            'issued_at': cert['issued_at'],
            'expires_at': cert['expires_at'],
            'is_valid': is_valid
        }
    
    def get_user_certificates(self, user_id: str) -> List[Dict]:
        """Get user certificates"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM certificates WHERE user_id = ?
            ORDER BY issued_at DESC
        ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_course_progress(self, user_id: str, course_id: str) -> Dict:
        """Get course progress"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get total modules
        cursor.execute('SELECT COUNT(*) FROM modules WHERE course_id = ?', (course_id,))
        total_modules = cursor.fetchone()[0]
        
        # Get completed modules (where user passed assessment)
        cursor.execute('''
            SELECT COUNT(DISTINCT m.module_id) 
            FROM modules m
            JOIN assessments a ON m.module_id = a.module_id
            JOIN assessment_results ar ON a.assessment_id = ar.assessment_id
            WHERE m.course_id = ? AND ar.user_id = ? AND ar.passed = 1
        ''', (course_id, user_id))
        
        completed_modules = cursor.fetchone()[0]
        conn.close()
        
        progress_percent = (completed_modules / total_modules * 100) if total_modules > 0 else 0
        
        return {
            'total_modules': total_modules,
            'completed_modules': completed_modules,
            'progress_percent': round(progress_percent, 2)
        }
