# 🚀 VULTURE v1.0.0 - Installation Guide

**تعليمات التثبيت الكاملة والصحيحة**

---

## 📋 المتطلبات الأساسية

```bash
Python: 3.9+ (3.10+ موصى به)
pip: 21.0+
git: 2.0+
```

### تحقق من إصدار Python:
```bash
python --version
# أو
python3 --version
```

---

## 🔧 خطوات التثبيت السريعة

### 1️⃣ استنساخ المشروع

```bash
git clone https://github.com/black-210/VULTURE.git
cd VULTURE
```

### 2️⃣ إنشاء بيئة افتراضية (مهم!)

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ ترقية pip

```bash
pip install --upgrade pip setuptools wheel
```

### 4️⃣ تثبيت المتطلبات

```bash
# التثبيت الأساسي
pip install -r requirements.txt

# أو التثبيت مع المتطلبات الإضافية
pip install -e .
```

### 5️⃣ التحقق من التثبيت

```bash
# اختبر استيراد المكتبات
python -c "import numpy; import scipy; import sklearn; print('✅ Basic imports OK')"

# اختبر VULTURE
python -c "from src.vulture import __version__; print(f'VULTURE v{__version__}')"
```

---

## 🎯 التثبيت المتقدم

### مع دعم GPU (CUDA)

```bash
# PyTorch مع CUDA 11.8
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# CuPy مع CUDA 11.x
pip install cupy-cuda11x

# تحقق من GPU
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
```

### مع دعم OpenAI API (للذكاء الاصطناعي)

```bash
pip install openai
export OPENAI_API_KEY="your-api-key-here"
```

### مع كل الميزات الاختيارية

```bash
pip install -e ".[gpu,ai,dev,medical,bio]"
```

---

## 🧪 تشغيل الاختبارات

```bash
# تشغيل جميع الاختبارات
pytest -v

# مع تقرير التغطية
pytest -v --cov=src --cov-report=html

# اختبار معين
pytest tests/test_rf_intelligence.py -v
```

### يجب أن ترى:
```
======================== test session starts =========================
collected 200+ items
test_core_framework.py::test_registry_basics PASSED
test_rf_intelligence.py::test_fft_analyzer PASSED
...
==================== 200+ passed in 15.42s ====================
```

---

## 🖥️ واجهة سطر الأوامر (CLI)

```bash
# معلومات النظام
python -m vulture.cli info

# تحليل RF
python -m vulture.cli rf --help

# تشغيل النماذج
python -m vulture.cli ml --help

# معالجة الإشارات
python -m vulture.cli dsp --help
```

---

## 🎨 واجهة المستخدم الرسومية (GUI)

```bash
# تشغيل الواجهة الرسومية
python -m vulture.gui

# مع وضع ملء الشاشة
python -m vulture.gui --fullscreen

# مع الوضع المفصل
python -m vulture.gui --verbose
```

### المتطلبات:
- PyQt6 (مثبت مسبقاً)
- شاشة بدقة 1920x1080 على الأقل (موصى به)

---

## 📦 هيكل المشروع بعد التثبيت

```
VULTURE/
├── src/vulture/                    ✅ الكود الأساسي
│   ├── __init__.py
│   ├── core/                       ✅ (10 modules)
│   ├── rf_intelligence/            ✅ (12 modules)
│   ├── sdr_iq_framework/           ✅ (10 modules)
│   ├── signal_processing/          ✅ (11 modules)
│   ├── ml_framework/               ✅ (8 modules)
│   ├── rf_fingerprinting_framework/✅ (7 modules)
│   ├── ai_intelligence_framework/  ✅ (6 modules)
│   ├── protocols_framework/        ✅ (6 modules)
│   ├── timeseries_framework/       ✅ (6 modules)
│   ├── visualization_advanced/     ✅ (6 modules)
│   ├── plugin_marketplace/         ✅ (5 modules)
│   └── support_system/             ✅ (4 modules)
│
├── tests/                          ✅ اختبارات شاملة
├── venv/                           (البيئة الافتراضية)
├── requirements.txt                (المتطلبات)
├── setup.py                        (إعدادات التثبيت)
├── pytest.ini                      (إعدادات الاختبارات)
└── README.md                       (التوثيق)
```

---

## 🐛 استكشاف الأخطاء

### المشكلة: `ModuleNotFoundError: No module named 'vulture'`

**الحل:**
```bash
# تأكد من تفعيل البيئة الافتراضية
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# أعد التثبيت
pip install -e .

# أضف المسار
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
```

### المشكلة: `ImportError: No module named 'PyQt6'`

**الحل:**
```bash
pip install --upgrade PyQt6
```

### المشكلة: مشاكل مع GPU

**الحل:**
```bash
# تحقق من CUDA
nvidia-smi

# أعد تثبيت PyTorch
pip uninstall torch -y
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### المشكلة: الاختبارات تفشل

**الحل:**
```bash
# حدّث المتطلبات
pip install --upgrade -r requirements.txt

# امسح الملفات المخزنة
find . -type d -name __pycache__ -exec rm -r {} +
find . -type f -name "*.pyc" -delete

# شغّل الاختبارات مجدداً
pytest -v --tb=short
```

---

## ✅ التحقق النهائي

```bash
# اختبار شامل
python << 'EOF'
print("=" * 50)
print("VULTURE v1.0.0 - Installation Verification")
print("=" * 50)

# 1. Core imports
try:
    from src.vulture import __version__
    print(f"✅ VULTURE Version: {__version__}")
except Exception as e:
    print(f"❌ Core import failed: {e}")

# 2. Framework imports
try:
    from src.vulture.core import FrameworkRegistry
    from src.vulture.rf_intelligence import *
    from src.vulture.signal_processing import *
    print("✅ All frameworks imported successfully")
except Exception as e:
    print(f"❌ Framework import failed: {e}")

# 3. Dependencies
try:
    import numpy as np
    import scipy
    import sklearn
    import pandas as pd
    import matplotlib
    import PyQt6
    print("✅ All dependencies available")
except Exception as e:
    print(f"❌ Dependency check failed: {e}")

# 4. Optional GPU support
try:
    import torch
    gpu = torch.cuda.is_available()
    print(f"✅ PyTorch available, GPU: {gpu}")
except:
    print("⚠️  PyTorch not installed (optional)")

print("=" * 50)
print("Installation Complete! 🚀")
print("=" * 50)
EOF
```

---

## 🚀 الخطوات التالية

### للمبتدئين:
1. اقرأ [README.md](README.md)
2. استكشف [examples/](examples/) directory
3. جرّب [CLI commands](#-واجهة-سطر-الأوامر-cli)

### للمطورين:
1. ادرس [Developer Guide](docs/developer_guide.md)
2. ساهم في [GitHub Issues](https://github.com/black-210/VULTURE/issues)
3. قدّم [Pull Requests](https://github.com/black-210/VULTURE/pulls)

### للباحثين:
1. استخدم [RF Intelligence Framework](src/vulture/rf_intelligence/)
2. استكشف [Signal Processing](src/vulture/signal_processing/)
3. جرّب [Machine Learning](src/vulture/ml_framework/)

---

## 📞 المساعدة والدعم

- **Documentation**: [docs/](docs/)
- **GitHub Issues**: [Report Bugs](https://github.com/black-210/VULTURE/issues)
- **Discussions**: [Ask Questions](https://github.com/black-210/VULTURE/discussions)
- **Email**: support@vulture.dev

---

## 📋 ملاحظات مهمة

⚠️ **تحذير أمان:**
- لا تشارك مفاتيح API أو كلمات السر
- استخدم متغيرات البيئة للمفاتيح الحساسة
- احذر من الملفات المشبوهة

✅ **أفضل الممارسات:**
- استخدم بيئة افتراضية دائماً
- بدّل المكتبات بشكل دوري
- قم بتشغيل الاختبارات قبل الإرسال

---

**تم تحديث الدليل:** 2026-08-16  
**إصدار VULTURE:** 1.0.0  
**الحالة:** ✅ جاهز للإنتاج
