"""Phase 2 Completion Tests"""
import pytest
from src.vulture.plugin_marketplace.registry import PluginRegistry
from src.vulture.plugin_marketplace.validator import PluginValidator
from src.vulture.plugin_marketplace.installer import PluginInstaller
from src.vulture.plugin_marketplace.api import MarketplaceAPI
from src.vulture.support_system.support_system import SupportTicket, KnowledgeBase, SLAManager
from src.vulture.certification_program.certification_program import CertificationProgram
from src.vulture.licensing_system.licensing_system import LicenseManager
import tempfile
import json
import os

class TestPluginMarketplace:
    """Test Plugin Marketplace"""
    
    def test_plugin_registry(self):
        """Test plugin registry"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            registry = PluginRegistry(db_path)
            
            # Register plugin
            success = registry.register_plugin(
                name='test-plugin',
                version='1.0.0',
                author='Test Author',
                description='Test Description',
                repository='https://github.com/test/test'
            )
            
            assert success
            
            # Get plugin
            plugin = registry.get_plugin('test-plugin')
            assert plugin is not None
            assert plugin['name'] == 'test-plugin'
            
            # Search
            results = registry.search_plugins('test')
            assert len(results) > 0
        
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_plugin_validator(self):
        """Test plugin validator"""
        # Valid manifest
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            manifest = {
                'name': 'test-plugin',
                'version': '1.0.0',
                'author': 'Test',
                'entry_point': 'test:TestPlugin'
            }
            json.dump(manifest, f)
            f.flush()
            
            try:
                valid, errors = PluginValidator.validate_manifest(f.name)
                assert valid
                assert len(errors) == 0
            finally:
                os.unlink(f.name)
    
    def test_plugin_installer(self):
        """Test plugin installer"""
        with tempfile.TemporaryDirectory() as tmpdir:
            installer = PluginInstaller(tmpdir)
            
            # List installed
            plugins = installer.list_installed()
            assert isinstance(plugins, list)

class TestSupportSystem:
    """Test Support System"""
    
    def test_support_tickets(self):
        """Test support ticket system"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            ticket_system = SupportTicket(db_path)
            
            # Create ticket
            ticket_id = ticket_system.create_ticket(
                user_id='user123',
                subject='Test Issue',
                description='This is a test',
                priority='high'
            )
            
            assert ticket_id.startswith('TICKET-')
            
            # Get ticket
            ticket = ticket_system.get_ticket(ticket_id)
            assert ticket is not None
            assert ticket['subject'] == 'Test Issue'
            
            # Update status
            success = ticket_system.update_status(ticket_id, 'in_progress', 'support_agent')
            assert success
            
            # Add comment
            success = ticket_system.add_comment(ticket_id, 'agent1', 'Working on it')
            assert success
        
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_knowledge_base(self):
        """Test knowledge base"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            kb = KnowledgeBase(db_path)
            
            # Add article
            article_id = kb.add_article(
                title='How to Install',
                content='Step 1, Step 2, ...',
                category='Getting Started'
            )
            
            assert article_id.startswith('KB-')
            
            # Get article
            article = kb.get_article(article_id)
            assert article is not None
            assert article['title'] == 'How to Install'
            
            # Search
            results = kb.search_articles('Install')
            assert len(results) > 0
        
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)
    
    def test_sla_manager(self):
        """Test SLA management"""
        from datetime import datetime
        
        ticket = {
            'priority': 'critical',
            'created_at': datetime.now().isoformat(),
            'status': 'open'
        }
        
        sla = SLAManager.check_sla_compliance(ticket)
        
        assert 'sla_hours' in sla
        assert sla['sla_hours'] == 1  # Critical: 1 hour
        assert 'is_compliant' in sla

class TestCertification:
    """Test Certification Program"""
    
    def test_certification_program(self):
        """Test certification program"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            cert = CertificationProgram(db_path)
            
            # Create course
            course_id = cert.create_course(
                name='RF Basics',
                description='Learn RF fundamentals',
                level='beginner',
                duration_hours=20
            )
            
            assert course_id.startswith('COURSE-')
            
            # Enroll user
            enrollment_id = cert.enroll_user('user123', course_id)
            assert enrollment_id.startswith('ENROLL-')
            
            # Get progress
            progress = cert.get_course_progress('user123', course_id)
            assert 'progress_percent' in progress
        
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

class TestLicensing:
    """Test Licensing System"""
    
    def test_license_manager(self):
        """Test license management"""
        with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
            db_path = f.name
        
        try:
            license_mgr = LicenseManager(db_path)
            
            # Create license
            license_key = license_mgr.create_license(
                organization='TestCorp',
                license_type='commercial',
                max_users=10,
                validity_days=365,
                features=['rf_analysis', 'ml_training']
            )
            
            assert license_key is not None
            assert license_key.startswith('VULTURE-')
            
            # Validate license
            validation = license_mgr.validate_license(license_key)
            assert validation['valid']
            assert validation['organization'] == 'TestCorp'
            
            # Log usage
            success = license_mgr.log_usage(license_key, 'user123', 'login')
            assert success
            
            # Generate invoice
            success = license_mgr.generate_invoice(license_key, 999.99)
            assert success
            
            # Get compliance report
            report = license_mgr.get_compliance_report(license_key)
            assert 'organization' in report
            assert 'usage_stats' in report
        
        finally:
            if os.path.exists(db_path):
                os.unlink(db_path)

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
