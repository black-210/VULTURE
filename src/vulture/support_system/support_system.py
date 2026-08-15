"""Support System - Tickets, Knowledge Base, SLA Management"""
import sqlite3
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class SupportTicket:
    """Support ticket system"""
    
    PRIORITIES = ['low', 'medium', 'high', 'critical']
    STATUSES = ['open', 'in_progress', 'waiting', 'resolved', 'closed']
    
    def __init__(self, db_path: str = 'support.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize support database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY,
                ticket_id TEXT UNIQUE NOT NULL,
                user_id TEXT NOT NULL,
                subject TEXT NOT NULL,
                description TEXT,
                priority TEXT DEFAULT 'medium',
                status TEXT DEFAULT 'open',
                assigned_to TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket_comments (
                id INTEGER PRIMARY KEY,
                ticket_id TEXT NOT NULL,
                author_id TEXT NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS attachments (
                id INTEGER PRIMARY KEY,
                ticket_id TEXT NOT NULL,
                file_name TEXT,
                file_path TEXT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (ticket_id) REFERENCES tickets(ticket_id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def create_ticket(self, user_id: str, subject: str, description: str, 
                     priority: str = 'medium') -> str:
        """Create support ticket"""
        import uuid
        ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO tickets (ticket_id, user_id, subject, description, priority)
            VALUES (?, ?, ?, ?, ?)
        ''', (ticket_id, user_id, subject, description, priority))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Ticket created: {ticket_id}")
        return ticket_id
    
    def update_status(self, ticket_id: str, status: str, assigned_to: str = None) -> bool:
        """Update ticket status"""
        if status not in self.STATUSES:
            return False
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        resolved_at = datetime.now() if status == 'resolved' else None
        
        cursor.execute('''
            UPDATE tickets 
            SET status = ?, assigned_to = ?, updated_at = ?, resolved_at = ?
            WHERE ticket_id = ?
        ''', (status, assigned_to, datetime.now(), resolved_at, ticket_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    def add_comment(self, ticket_id: str, author_id: str, comment: str) -> bool:
        """Add comment to ticket"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO ticket_comments (ticket_id, author_id, comment)
                VALUES (?, ?, ?)
            ''', (ticket_id, author_id, comment))
            
            # Update ticket timestamp
            cursor.execute('''
                UPDATE tickets SET updated_at = ? WHERE ticket_id = ?
            ''', (datetime.now(), ticket_id))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            return False
    
    def get_ticket(self, ticket_id: str) -> Optional[Dict]:
        """Get ticket details"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM tickets WHERE ticket_id = ?', (ticket_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return dict(row)
        return None
    
    def get_user_tickets(self, user_id: str, status: str = None) -> List[Dict]:
        """Get user tickets"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        if status:
            cursor.execute('''
                SELECT * FROM tickets 
                WHERE user_id = ? AND status = ?
                ORDER BY created_at DESC
            ''', (user_id, status))
        else:
            cursor.execute('''
                SELECT * FROM tickets 
                WHERE user_id = ?
                ORDER BY created_at DESC
            ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_comments(self, ticket_id: str) -> List[Dict]:
        """Get ticket comments"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM ticket_comments 
            WHERE ticket_id = ?
            ORDER BY created_at ASC
        ''', (ticket_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


class KnowledgeBase:
    """Knowledge base and documentation"""
    
    def __init__(self, db_path: str = 'kb.db'):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize knowledge base"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY,
                article_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                content TEXT,
                category TEXT,
                views INTEGER DEFAULT 0,
                helpful_count INTEGER DEFAULT 0,
                unhelpful_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                icon TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def add_article(self, title: str, content: str, category: str) -> str:
        """Add knowledge base article"""
        import uuid
        article_id = f"KB-{uuid.uuid4().hex[:8].upper()}"
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO articles (article_id, title, content, category)
            VALUES (?, ?, ?, ?)
        ''', (article_id, title, content, category))
        
        conn.commit()
        conn.close()
        
        return article_id
    
    def search_articles(self, query: str) -> List[Dict]:
        """Search knowledge base"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM articles 
            WHERE title LIKE ? OR content LIKE ?
            ORDER BY views DESC
        ''', (f'%{query}%', f'%{query}%'))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_article(self, article_id: str) -> Optional[Dict]:
        """Get article"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM articles WHERE article_id = ?', (article_id,))
        row = cursor.fetchone()
        
        if row:
            # Increment view count
            cursor.execute('''
                UPDATE articles SET views = views + 1 WHERE article_id = ?
            ''', (article_id,))
            conn.commit()
        
        conn.close()
        
        return dict(row) if row else None
    
    def mark_helpful(self, article_id: str, helpful: bool) -> bool:
        """Mark article as helpful/unhelpful"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            if helpful:
                cursor.execute('''
                    UPDATE articles SET helpful_count = helpful_count + 1 
                    WHERE article_id = ?
                ''', (article_id,))
            else:
                cursor.execute('''
                    UPDATE articles SET unhelpful_count = unhelpful_count + 1 
                    WHERE article_id = ?
                ''', (article_id,))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error marking article: {e}")
            return False


class SLAManager:
    """Service Level Agreement management"""
    
    # SLA times in hours
    SLA_TIMES = {
        'critical': 1,
        'high': 4,
        'medium': 24,
        'low': 72
    }
    
    @staticmethod
    def check_sla_compliance(ticket: Dict) -> Dict:
        """Check if ticket meets SLA"""
        priority = ticket['priority']
        sla_hours = SLAManager.SLA_TIMES.get(priority, 24)
        
        created_at = datetime.fromisoformat(ticket['created_at'])
        time_elapsed = (datetime.now() - created_at).total_seconds() / 3600
        
        is_compliant = time_elapsed <= sla_hours
        
        return {
            'priority': priority,
            'sla_hours': sla_hours,
            'time_elapsed_hours': round(time_elapsed, 2),
            'is_compliant': is_compliant,
            'time_remaining_hours': max(0, round(sla_hours - time_elapsed, 2))
        }
    
    @staticmethod
    def generate_sla_report(tickets: List[Dict]) -> Dict:
        """Generate SLA compliance report"""
        total = len(tickets)
        compliant = 0
        
        by_priority = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        compliant_by_priority = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
        
        for ticket in tickets:
            sla = SLAManager.check_sla_compliance(ticket)
            priority = ticket['priority']
            
            by_priority[priority] = by_priority.get(priority, 0) + 1
            
            if sla['is_compliant']:
                compliant += 1
                compliant_by_priority[priority] = compliant_by_priority.get(priority, 0) + 1
        
        compliance_rate = (compliant / total * 100) if total > 0 else 0
        
        return {
            'total_tickets': total,
            'compliant_tickets': compliant,
            'compliance_rate': round(compliance_rate, 2),
            'by_priority': by_priority,
            'compliant_by_priority': compliant_by_priority
        }
