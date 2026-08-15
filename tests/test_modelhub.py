import tempfile
import os
from vulture.modelhub.repo import ModelHub
from vulture.modelhub.verify import compute_sha256


def test_modelhub_add_and_verify(tmp_path):
    # create fake model file
    p = tmp_path / "m.onnx"
    p.write_bytes(b"dummy-model")
    hub = ModelHub(base_dir=str(tmp_path))
    dest = hub.add_model(str(p), name="dummy")
    assert os.path.exists(dest)
    sha = compute_sha256(dest)
    assert hub.verify_hash('dummy', sha)
