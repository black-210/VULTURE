"""Optional receive-only hardware smoke tests for approved lab devices.

Run explicitly with RF_DNA_LAB_HARDWARE=1 and a configured device; CI skips by default.
"""
import os
import pytest


@pytest.mark.hardware
@pytest.mark.skipif(os.getenv("RF_DNA_LAB_HARDWARE") != "1", reason="approved lab hardware not enabled")
def test_soapysdr_receive_backend_is_explicit():
    from vulture.rf_dna.sdr_adapter import ReceiveConfig, ReceiveOnlySource
    source = ReceiveOnlySource(ReceiveConfig(1_000_000, 100_000_000, device_args=os.getenv("RF_DNA_SOAPY_ARGS")))
    assert source.config.device_args


@pytest.mark.hardware
@pytest.mark.skipif(os.getenv("RF_DNA_LAB_HARDWARE") != "1", reason="approved lab hardware not enabled")
def test_uhd_import_is_optional():
    pytest.importorskip("uhd")
