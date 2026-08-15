import pytest

pytest.importorskip('rtlsdr')
from vulture.sdr.rtl import RTLSDRDevice


def test_rtl_device_interface():
    # we cannot actually access hardware in CI; this test ensures the class exists and start raises if not available
    dev = RTLSDRDevice(cfg={'sample_rate': 2.4e6})
    # starting without hardware may raise RuntimeError if pyrtlsdr not functional in environment
    try:
        dev.start()
    except RuntimeError:
        pytest.skip('RTLSDR hardware not available')
    finally:
        try:
            dev.stop()
        except Exception:
            pass
