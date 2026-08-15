"""Phase 3 Final Integration Tests"""
import pytest
import tempfile
import os
import json
import numpy as np
from datetime import datetime

from src.vulture.timeseries_framework.timeseries_framework import TimeseriesAnalyzer
from src.vulture.visualization_advanced.visualization_advanced import SignalAnatomy
from src.vulture.physics_laboratory.physics_laboratory import Electromagnetic, LinkBudget
from src.vulture.plugin_marketplace.api import MarketplaceAPI
from src.vulture.support_system.support_system import SupportTicket, KnowledgeBase
from src.vulture.certification_program.certification_program import CertificationProgram
from src.vulture.licensing_system.licensing_system import LicenseManager

class TestPhase3Integration:
    """Test Phase 3 - Full Enterprise Integration"""
    
    def test_end_to_end_enterprise_workflow(self):
        """Test complete enterprise workflow"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Initialize all systems
            license_mgr = LicenseManager(os.path.join(tmpdir, 'licenses.db'))
            cert_program = CertificationProgram(os.path.join(tmpdir, 'certs.db'))
            support_system = SupportTicket(os.path.join(tmpdir, 'support.db'))
            marketplace = MarketplaceAPI(
                os.path.join(tmpdir, 'marketplace.db'),
                os.path.join(tmpdir, 'plugins')
            )
            
            # 1. Create enterprise license
            license_key = license_mgr.create_license(
                organization='Enterprise Corp',
                license_type='enterprise',
                max_users=100,
                validity_days=365,
                features=['full_access', 'support', 'training']
            )
            assert license_key is not None
            
            # 2. Create training course
            course_id = cert_program.create_course(
                name='Enterprise VULTURE Training',
                description='Complete training program',
                level='intermediate',
                duration_hours=40
            )
            assert course_id is not None
            
            # 3. Create support ticket
            ticket_id = support_system.create_ticket(
                user_id='enterprise_user',
                subject='Integration assistance',
                description='Need help with setup',
                priority='high'
            )
            assert ticket_id is not None
            
            # 4. Verify all systems work together
            license_valid = license_mgr.validate_license(license_key)['valid']
            assert license_valid
            
            ticket = support_system.get_ticket(ticket_id)
            assert ticket['status'] == 'open'
            
            enrollment = cert_program.enroll_user('enterprise_user', course_id)
            assert enrollment is not None
    
    def test_analytics_pipeline(self):
        """Test complete analytics pipeline"""
        # Create signal data
        t = np.linspace(0, 10, 1000)
        signal = np.sin(2 * np.pi * 0.5 * t) + 0.5 * np.cos(2 * np.pi * 2 * t)
        signal += np.random.normal(0, 0.1, len(signal))
        
        # Analyze with Timeseries
        analyzer = TimeseriesAnalyzer()
        components = analyzer.decompose(signal, period=100)
        assert components is not None
        
        # Visualize with advanced tools
        anatomy = SignalAnatomy()
        anatomy_result = anatomy.decompose_signal(signal)
        assert anatomy_result is not None
        
        # Physics calculations
        # Calculate RF propagation
        em = Electromagnetic()
        wavelength = em.wavelength(2.4e9)
        assert wavelength > 0
        
        # Link budget
        link_budget = LinkBudget.calculate_link_budget(
            tx_power_dbm=20,
            tx_gain_db=12,
            rx_gain_db=12,
            path_loss_db=100
        )
        assert link_budget['received_power_dbm'] is not None
    
    def test_marketplace_certification_integration(self):
        """Test marketplace and certification integration"""
        with tempfile.TemporaryDirectory() as tmpdir:
            marketplace = MarketplaceAPI(
                os.path.join(tmpdir, 'marketplace.db'),
                os.path.join(tmpdir, 'plugins')
            )
            cert_program = CertificationProgram(os.path.join(tmpdir, 'certs.db'))
            
            # Create certified course
            course_id = cert_program.create_course(
                name='Plugin Development Certification',
                description='Learn to develop VULTURE plugins',
                level='advanced',
                duration_hours=30
            )
            
            # Enroll users
            enrollment1 = cert_program.enroll_user('dev1', course_id)
            enrollment2 = cert_program.enroll_user('dev2', course_id)
            
            assert enrollment1 is not None
            assert enrollment2 is not None
    
    def test_full_system_health(self):
        """Test overall system health"""
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Initialize all components
                components = {
                    'timeseries': TimeseriesAnalyzer(),
                    'visualization': SignalAnatomy(),
                    'physics': Electromagnetic(),
                    'licensing': LicenseManager(os.path.join(tmpdir, 'licenses.db')),
                    'support': SupportTicket(os.path.join(tmpdir, 'support.db')),
                    'certification': CertificationProgram(os.path.join(tmpdir, 'certs.db')),
                    'marketplace': MarketplaceAPI(
                        os.path.join(tmpdir, 'marketplace.db'),
                        os.path.join(tmpdir, 'plugins')
                    )
                }
                
                # Verify all components initialized successfully
                assert len(components) == 7
                assert all(v is not None for v in components.values())
                
                # Quick functionality check
                # Timeseries
                data = np.random.randn(100)
                ts_result = components['timeseries'].decompose(data)
                assert ts_result is not None
                
                # Licensing
                license_key = components['licensing'].create_license(
                    'Health Check Org',
                    'trial',
                    10,
                    30
                )
                assert license_key is not None
                
                # Support
                ticket = components['support'].create_ticket(
                    'health_check_user',
                    'System Health Check',
                    'Performing system health check'
                )
                assert ticket is not None
                
                # Certification
                course = components['certification'].create_course(
                    'Health Check Course',
                    'Verifying certification system',
                    'beginner',
                    5
                )
                assert course is not None
                
                print("✅ All Phase 3 components healthy and operational")
                return True
            
            except Exception as e:
                print(f"❌ System health check failed: {e}")
                raise

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
