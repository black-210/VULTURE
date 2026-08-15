# VULTURE 🦅

Comprehensive toolkit for RF, SDR, signal processing, and AI-powered analysis.

[![CI](https://github.com/black-210/VULTURE/actions/workflows/ci.yml/badge.svg)](https://github.com/black-210/VULTURE/actions/workflows/ci.yml)
[![Quality](https://github.com/black-210/VULTURE/actions/workflows/quality.yml/badge.svg)](https://github.com/black-210/VULTURE/actions/workflows/quality.yml)

## نظرة عامة / Overview

VULTURE هو مشروع يستخدم مجموعة من الأطر (frameworks) للعمل مع إشارات الراديو، أجهزة SDR، معالجة الإشارة، وتعلّم الآلة، بالإضافة إلى واجهات وملحقات (plugins) ودمج مع نماذج الذكاء الاصطناعي.

This repository currently provides scaffolding and initial implementations (stubs and minimal working examples) across the following domains:

- CORE ENGINE — framework registry, DI, configuration manager, plugin system, security policy (scaffold)
- AI INTELLIGENCE FRAMEWORK — LLM router, vision adapter, code-generation engine, tool executor, memory manager (scaffold)
- RF INTELLIGENCE FRAMEWORK — FFT/PSD, spectrogram, waterfall, peak/burst/noise detection, anomaly detection
- SDR / IQ FRAMEWORK — hardware abstraction, IQ IO (NPY/BIN/WAV), format detection, metadata
- SIGNAL PROCESSING FRAMEWORK — filters, windows, convolution/correlation, GPU fallback
- ML / DEEP LEARNING FRAMEWORK — preprocessing, feature engineering, training wrappers, PyTorch/ONNX helpers
- RF FINGERPRINTING FRAMEWORK — feature extraction, clustering, classification, anomaly detection
- DATASET INTELLIGENCE FRAMEWORK — CSV/JSON/Parquet/NPY loaders, validation, transforms
- PLUGIN & MODEL HUB frameworks — stubs for plugin discovery, sandboxing, and local model repository
- CLI — `vulture` command with subcommands (info, sdr, rf, ml, dsp, gui)
- PyQt6 GUI — multi-tab GUI scaffold (placeholder)

ملاحظة: معظم الموديولات حاليًا عبارة عن "stubs" قابلة للتوسيع مع fallbacks إن لم تتوفر المكتبات الاختيارية مثل numpy/pandas/sklearn/torch.

---

## Quick start

Requirements
- Python 3.8+
- Optional packages (for full functionality): numpy, scipy, pandas, scikit-learn, torch, matplotlib

Install (recommended in a virtualenv)

```bash
python -m venv .venv
source .venv/bin/activate  # macOS / Linux
.venv\\Scripts\\activate     # Windows PowerShell
python -m pip install --upgrade pip
pip install -r requirements.txt  # optional, repository does not yet include a full requirements file
pip install pytest
```

Run tests

```bash
git checkout feature/add-scaffold
pytest -q
```

Run basic CLI

```bash
python -m vulture.main --help
python -m vulture.main --verbose
```

---

## Modules and how to use them (short docs)

Each subpackage exposes simple, well-documented functions/classes. Below are short examples and where to find them.

### Core
- `vulture/__init__.py` — package metadata and __version__
- `vulture/main.py` — entrypoint; calls CLI and services
- `vulture/cli.py` — argparse-based CLI
- `vulture/config.py` — `load_config(path)` returns dictionary of config values
- `vulture/utils.py` — `setup_logging(verbose)` returns logger
- `vulture/services.py` — `run(args)` main runner (placeholder)

Example
```py
from vulture.cli import parse_args
from vulture.services import run
args = parse_args()
res = run(args)
print(res)
```

### SPECTRUM INTELLIGENCE FRAMEWORK — Spectrum Intelligence
- Real-time Spectrum Analysis — معالجة طيفية في الوقت الحقيقي: استقبال إطارات IQ، حساب FFT/PSD، وتوليد بيانات الطيف اللازمة للمراقبة واكتشاف التداخل.
- Frequency Allocation Visualization — عرض وتصور تخصيص الطيف بتسميات القنوات/النطاقات لتسهيل متابعة التخصيصات والتداخلات المحتملة.
- Interference Detection — كشف التداخلات والاشتباكات الطيفية عبر قواعد عتبية أو خوارزميات كشف الشذوذ.
- Spectrum Monitoring — رصد مستمر للطيف مع تخزين مؤشرات الأداء والإنذارات.

Files: `vulture/spectrum/*`
- `RealTimeAnalyzer` — process_frame(iq_frame) returns spectrum, peaks, metadata.
- `SpectrumVisualizer` — render_spectrum(spectrum_data, out_path)

مثال مختصر (مثال بالعربي)
```py
from vulture.spectrum.real_time import RealTimeAnalyzer
ana = RealTimeAnalyzer(sample_rate=2.4e6)
res = ana.process_frame(iq_frame)
print(res['meta'])
```

### PHYSICS LABORATORY
- Electromagnetic Calculations — حسابات فيزيائية أساسية لكهربية ومغناطيسية الموجات.
- Link Budget Analysis — تحليل ميزانية الرابط: حساب خسائر المسار، الربح، وpower at receiver.
- Antenna Calculations — حسابات للصيغة الفعّالة للمجال، الفتحة الفعالة، والربح.
- Propagation Models — نماذج الانتشار (حرّة، نموذج Hata، ITU) كمراجع أولية.

Files: `vulture/physics/*`
- `Antenna` — simple antenna helpers, `effective_area()`
- `LinkBudget` — `estimate_rx_power_dbm(freq_hz, distance_m)`

مثال
```py
from vulture.physics.antenna import Antenna
ant = Antenna(gain_dbi=8, frequency_hz=2.4e9)
print(ant.effective_area())
```

### DATASET INTELLIGENCE FRAMEWORK
- Multi-Format Support (CSV, JSON, Parquet, HDF5, NPY, SigMF) — دعم تحميل البيانات من صيغ متعددة، مع fallbacks إن لم تكن مكتبات معينة متاحة.
- Data Validation & Profiling — أدوات بسيطة للتحقق من شكل البيانات وجودتها (validate_schema، profiling لاحقاً).
- Cleaning & Transformation — تنظيف القيم المفقودة، تحويلات مبدئية، ووظائف تقسيم البيانات.
- Train/Test Splitting — تقسيم بيانات التدريب والاختبار مع دعم sklearn إن توفر.

Files: `vulture/dataset/*`
- Loaders: `load_csv`, `load_json`, `load_npy`, `load_parquet` (depend on pandas/numpy)
- `validate_schema(dataset, schema)` — simple schema validator
- `train_test_split`, `clean_missing` — transform helpers

مثال
```py
from vulture.dataset.io import load_csv
df = load_csv('data/example.csv')
```

### SDR / IQ
Files: `vulture/sdr/*`
- `HardwareInterface` — abstract device API (start, stop, read_samples)
- `IQRecorder`, `IQPlayer` — record/playback helpers
- `detect_format(path)` — returns npy/bin/wav or None
- `extract_metadata(path)` — placeholder metadata extractor

### Signal Processing (DSP)
Files: `vulture/dsp/*`
- `fft`, `ifft` — wrappers around numpy FFT
- `compute_psd` — PSD placeholder (welch/methods TODO)
- `apply_filter` — placeholder for FIR/IIR filters
- `get_window` — returns Hann/Hamming/Blackman windows
- `generate_spectrogram` — placeholder generating times/freqs/Sxx

Example
```py
from vulture.dsp.fft import fft
import numpy as np
x = np.random.randn(1024)
X = fft(x)
```

### Dataset Intelligence
Files: `vulture/dataset/*`
- Loaders: `load_csv`, `load_json`, `load_npy`, `load_parquet` (depend on pandas/numpy)
- `validate_schema(dataset, schema)` — simple schema validator
- `train_test_split`, `clean_missing` — transform helpers

### ML / Deep Learning
Files: `vulture/ml/*`
- Preprocessing: `scale_minmax`, `standardize`, `to_tensor`
- Feature extraction: `extract_basic_features`
- `Trainer` wrapper for sklearn-like models
- Validation: `compute_metrics`
- PyTorch helpers: `to_torch_tensor`, `save_model_onnx`
- GPU detection: `detect_gpu`

Example
```py
from vulture.ml.features import extract_basic_features
feats = extract_basic_features([0,1,2,3])
```

### RF Fingerprinting
Files: `vulture/fingerprinting/*`
- `extract_fingerprint_features(signal, sample_rate)` — statistical + spectral proxies
- `cluster_features` — KMeans/DBSCAN wrapper with fallbacks
- `train_classifier`, `predict_classifier` — RF/SVM wrappers, fallback dummy predictor
- `detect_anomalies` — IsolationForest wrapper or fallback

### Plugins & Model Hub (scaffold)
- Plugin discovery and sandboxing are scaffolded in `vulture/plugins` (placeholders)
- Model hub: local model repository helpers (stubs)

### CLI
The package exposes a CLI skeleton. Use `vulture.main` as the entrypoint; subcommands are to be implemented.

### GUI
PyQt6 GUI scaffold is present under `vulture/gui` (placeholders). Implement panels and wiring to backends as needed.

---

## Tests
Tests live under `tests/` (unit tests for core, ml, fingerprinting). To run:

```bash
pytest -q
```

CI runs on GitHub Actions (see `.github/workflows/ci.yml`) and performs test matrix across Python versions.

---

## Contributing
- Create issues for feature requests or bugs.
- Work on `feature/*` branches, open PRs to `main`.
- Follow code style: use `black` and `ruff` (pre-commit config is provided).

Suggested workflow

```bash
git checkout -b feature/my-feature
# make changes
git add .
git commit -m "feat: ..."
git push origin feature/my-feature
# open PR on GitHub
```

---

## Roadmap / Next steps
- Implement concrete SDR hardware adapters (RTL-SDR, UHD, PlutoSDR).
- Replace DSP placeholders with optimized implementations (scipy.signal, numba, cupy).
- Build a production-grade ML training loop (PyTorch) with dataset pipelines and on-disk model hub.
- Implement plugin permission model and sandboxed plugin executor.
- Add examples, documentation pages, and a demo GUI application.

---

## NEWS / Change log
See `NEWS.md` for a summarized changelog and batch descriptions.

---

## License
This repository uses the GNU Affero General Public License v3.0 (AGPL-3.0). See `LICENSE` or repository settings for full text.


---

If you want, I can now:
- open a Pull Request from `feature/add-scaffold` → `main`, with this README and all changes; or
- continue with Batch 6 (Plugin / Model Hub / CLI enhancements); or
- translate README contents fully to Arabic.
