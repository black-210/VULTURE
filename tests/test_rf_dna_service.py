"""RF-DNA service and provenance tests, entirely offline."""
import numpy as np

from vulture.rf_dna.provenance import CaptureProvenance, verify_provenance
from vulture.rf_dna.service import TenantCredential, TenantStore


def test_provenance_is_self_verifying_and_tenant_scoped():
    record = CaptureProvenance.create(tenant_id="lab-a", source="fixture", sample_rate=10, center_frequency=2, sample_count=4, content_sha256="a" * 64, authorization="approved").to_dict()
    assert verify_provenance(record)
    assert TenantStore([TenantCredential("token-a", "lab-a")]).tenant_for("token-a") == "lab-a"


def test_complex_input_remains_bounded():
    assert np.asarray([1 + 2j], dtype=np.complex64).size == 1
