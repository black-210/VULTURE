# 🦅 دليل استخدام VULTURE الشامل

## المحتويات
1. [مقدمة عامة](#مقدمة-عامة)
2. [أوامر SDR (جهاز الاستقبال)](#أوامر-sdr-جهاز-الاستقبال)
3. [أوامر التحليل الجنائي](#أوامر-التحليل-الجنائي)
4. [أوامر RF الكيميائي](#أوامر-rf-الكيميائي)
5. [أوامر RF-DNA](#أوامر-rf-dna)
6. [الواجهة التفاعلية](#الواجهة-التفاعلية)
7. [حل الأخطاء البرمجية](#حل-الأخطاء-البرمجية)

---

## مقدمة عامة

**VULTURE** منصة علمية متخصصة في:
- 📡 استقبال وتحليل إشارات RF (موضع الاستقبال فقط - لا يوجد بث)
- 🧪 التحليل الكيميائي والفيزيائي
- 🔬 تحليل الأجهزة للكشف عن الاختراق
- 📊 تحليل بصمات RF-DNA
- 🛡️ تقييم الثغرات الأمنية

### الملفات المدعومة
- ✅ `.npz` (NumPy Compressed Format)
- ✅ `.iq` (IQ Samples Format)

### الأمان
- ❌ لا اتصال بالشبكة (Offline Mode)
- ❌ لا بث RF (Receive Only)
- ❌ تحليل محلي فقط
- ✅ معالجة البيانات على الآلة المحلية

---

## أوامر SDR (جهاز الاستقبال)

### 1️⃣ التحقق من حالة الأجهزة

```bash
vulture sdr status
```

**الوصف:** يعرض قائمة بالأجهزة المتوفرة (RTL-SDR, HackRF, USRP)

**مثال على النتيجة:**
```json
{
  "available_devices": {
    "rtl-sdr": [{"available": true, "device_index": 0}],
    "hackrf": [{"available": true}],
    "usrp": [{"available": true, "index": 0}]
  },
  "receive_only": true,
  "transmission_disabled": true
}
```

**ما الذي يحدث:**
- ✅ فحص الأجهزة المتاحة
- ✅ التحقق من تعطيل وضع البث
- ✅ إرجاع معلومات كل جهاز

---

### 2️⃣ الحصول على معلومات الجهاز

```bash
vulture sdr info --device rtl-sdr
```

**المعاملات:**
- `--device`: نوع الجهاز (rtl-sdr | hackrf | usrp)

**مثال على النتيجة:**
```json
{
  "device_type": "rtl-sdr",
  "model": "RTL-SDR (DVB-T)",
  "driver_loaded": true,
  "frequency_range_hz": [24000000, 1766000000],
  "gain_range_db": [0, 50],
  "sample_rate_range_hz": [225001, 3200000]
}
```

**الفائدة:**
- معرفة نطاق التردد المدعوم
- معرفة مدى كسب الاستقبال
- التحقق من معدل العينات الممكن

---

### 3️⃣ التقاط بيانات RF

```bash
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --duration 5 \
  --output capture.npz
```

**المعاملات الهامة:**
| المعامل | الوصف | مثال |
|--------|-------|------|
| `--frequency-hz` | التردد (Hz) | 433920000 (433.92 MHz) |
| `--sample-rate` | معدل العينات (Hz) | 2400000 (2.4 Msps) |
| `--gain-db` | كسب الاستقبال (dB) | 20 |
| `--duration` | المدة (ثانية) | 5 |
| `--output` | اسم الملف | capture.npz |

**مثال على النتيجة:**
```
✓ Capture complete!
{
  "capture_path": "/home/user/capture.npz",
  "center_frequency_hz": 433920000,
  "sample_rate_actual": 2400000,
  "samples_collected": 12000000,
  "duration_seconds": 5
}
```

**الملف المُنشأ:**
- `capture.npz` يحتوي على:
  - `iq`: عينات IQ (12 مليون عينة)
  - `sample_rate`: 2400000
  - `center_frequency`: 433920000

---

### 4️⃣ مسح نطاق تردد

```bash
vulture sdr scan \
  --device rtl-sdr \
  --freq-start 88000000 \
  --freq-stop 108000000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --step-hz 1000000
```

**المعاملات:**
- `--freq-start`: تردد البداية (Hz)
- `--freq-stop`: تردد النهاية (Hz)
- `--step-hz`: حجم الخطوة (Hz) - افتراضي: 1000000

**مثال على النتيجة:**
```
Scanning 88 - 108 MHz on rtl-sdr

Frequency Scan Results:
Frequency (MHz) | Signal Strength (dBm)
------------------------------------------
       88.0   |               -75.3
       89.0   |               -65.2
       ...
      108.0   |               -82.3
```

---

## أوامر التحليل الجنائي

### 5️⃣ تحليل اختراق الجهاز

```bash
vulture forensic device \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000
```

**المعاملات المطلوبة:**
- `--input`: ملف التقاط (.npz أو .iq)
- `--case-id`: معرف القضية
- `--subject`: معرف الجهاز
- `--frequency-hz`: التردد المركزي

**المعاملات الاختيارية:**
- `--output`: مسار الملف (اختياري)
- `--format`: json | txt (افتراضي: json)

**ما يتم الكشف عنه:**
🔴 **مؤشرات الاختراق:**
- انحراف التردد (Frequency Drift)
- شذوذ القدرة (Power Anomaly)
- شذوذ التوقيت (Timing Anomaly)
- بصمات البرامج الضارة

🟠 **الثغرات الأمنية:**
| الكود | الوصف | الخطورة |
|------|-------|---------|
| RF-001 | قدرة ذروة عالية غير عادية | MEDIUM |
| RF-002 | انحراف التردد | HIGH |
| RF-003 | تشويش/تداخل محتمل | CRITICAL |
| RF-004 | عدم توازن I/Q | MEDIUM |
| PHY-001 | قوة إشارة ضعيفة | LOW |
| PHY-002 | قطع الإشارة | MEDIUM |
| PHY-003 | انزياح DC | LOW |

**مثال على النتيجة:**
```
╔═══════════════════════════════════════════════════════════╗
║         VULTURE FORENSIC COMPROMISE ANALYSIS REPORT      ║
╚═══════════════════════════════════════════════════════════╝

Case ID:              C-001
Device:               device-01
Status:               🔴 COMPROMISED
Compromise Score:     62.5/100
Confidence:           75.0%

Indicators Detected:
  • frequency-drift
  • power-anomaly
  • timing-anomaly

Total Findings:       8
  🔴 Critical:        1
  🟠 High:            2
  🟡 Medium:          3
  🔵 Low:             2
```

---

### 6️⃣ إنشاء تقرير جنائي شامل

```bash
vulture forensic report \
  --input capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000 \
  --output device-report.json \
  --format json
```

**الخيارات المتاحة:**
- `--format json`: تقرير JSON كامل
- `--format txt`: تقرير نصي مقروء
- `--format html`: تقرير HTML للعرض

---

### 7️⃣ تدقيق الفيزياء

```bash
vulture forensic physics \
  --case-id C-002 \
  --subject test-device \
  --frequency-hz 2400000000 \
  --distance-m 10 \
  --bandwidth-hz 20000000
```

**ما يتحقق منه:**
- ✅ التردد موجب وضمن النطاق
- ✅ المسافة موجبة وواقعية
- ✅ النطاق الترددي لا يتجاوز 2x التردد المركزي
- ✅ حساب خسارة المسار الحر

---

### 8️⃣ تدقيق الكيمياء

```bash
vulture forensic chemistry \
  --case-id C-003 \
  --subject sample-01 \
  --compounds-json '[{"name":"lead","concentration_ppm":2500},{"name":"mercury","concentration_ppm":150}]'
```

**المواد الخطرة المكتشفة:**
| المادة | الحد الآمن | السمية | الإجراء |
|--------|----------|--------|--------|
| الرصاص (Lead) | 1000 ppm | 85/100 | تجنب التعامل |
| الزئبق (Mercury) | 100 ppm | 90/100 | تجنب التعامل |
| الكادميوم (Cadmium) | 500 ppm | 88/100 | تجنب التعامل |
| البريليوم (Beryllium) | 50 ppm | 92/100 | تجنب التعامل |
| الأسبستوس (Asbestos) | 10 ppm | 95/100 | تجنب التعامل |

**الخطورة:** 🔴 CRITICAL إذا كانت التركيز أعلى من الحد الآمن

---

### 9️⃣ تدقيق الرياضيات

```bash
vulture forensic math \
  --case-id C-004 \
  --subject system-01 \
  --matrix-json '[[2,1],[1,1]]' \
  --vector-json '[3,2]'
```

**ما يتحقق منه:**
- ✅ أبعاد المصفوفة والمتجه متطابقة
- ✅ عدم وجود قيم غير نهائية (NaN, Inf)
- ✅ صحة حل النظام الخطي

---

### 🔟 تدقيق البروتوكول

```bash
vulture forensic protocol \
  --case-id C-005 \
  --subject frame-01 \
  --frames-json '[{"length":4,"checksum":"valid"}]'
```

**ما يتحقق منه:**
- ✅ طول الإطار صحيح
- ✅ Checksum صحيح
- ✅ لا يوجد اختراق الشبكة

---

## أوامر RF الكيميائي

### 1️⃣1️⃣ تحليل NMR

```bash
vulture chemical-rf nmr \
  --input capture.npz \
  --nucleus 1H \
  --field-t 7.0
```

**ما يحدث:**
- حساب تردد Larmor للنواة المحددة
- حسب المجال المغناطيسي
- استخدام معدل العينات من ملف الالتقاط

**النوى المدعومة:**
- `1H` (الهيدروجين)
- `13C` (الكربون 13)
- `31P` (الفسفور 31)

---

### 1️⃣2️⃣ تحليل الخصائص المادية

```bash
vulture chemical-rf material \
  --input capture.npz \
  --epsilon-r 4.2 \
  --conductivity 0.01 \
  --frequency-hz 2400000000 \
  --length-m 0.1
```

**المعاملات:**
- `--epsilon-r`: السماحية النسبية
- `--conductivity`: التوصيلية الكهربائية (S/m)
- `--frequency-hz`: التردد
- `--length-m`: طول المادة

**النتيجة تشمل:**
- السماحية المعقدة
- تردد الرنين
- خصائص المادة الديناميكية

---

### 1️⃣3️⃣ حسابات الفيزياء الكهرومغناطيسية

```bash
vulture chemical-rf physics \
  --input capture.npz \
  --frequency-hz 2400000000 \
  --distance-m 10
```

**يحسب:**
- الطول الموجي (Wavelength)
- خسارة المسار الحر (Path Loss)
- القوة المستقبلة

---

## أوامر RF-DNA

### 1️⃣4️⃣ حالة RF-DNA

```bash
vulture rf-dna status
```

---

### 1️⃣5️⃣ محاكاة RF-DNA

```bash
vulture rf-dna simulate \
  --profile multi-tone \
  --duration 2 \
  --sample-rate 1000000 \
  --seed 7 \
  --output capture.npz
```

**الملفات المحاكاة:**
- `noise`: ضوضاء عشوائية
- `multi-tone`: إشارات متعددة

---

### 1️⃣6️⃣ بصمة RF-DNA

```bash
vulture rf-dna fingerprint \
  --input capture.npz \
  --label device-01
```

**ما يستخرج:**
- بصمة فريدة للجهاز
- المقاييس الإحصائية
- Digest (معرف البصمة)

---

### 1️⃣7️⃣ لوحة المعلومات

```bash
vulture rf-dna dashboard \
  --input capture.npz \
  --label dashboard-capture
```

---

### 1️⃣8️⃣ تقرير RF-DNA

```bash
vulture rf-dna report \
  --input capture.npz \
  --label capture-report
```

---

## الواجهة التفاعلية

### دخول الوضع التفاعلي

```bash
vulture --interactive
```

**الواجهة:**
```
══════════════════════════════════════════════════════════════
🦅 VULTURE — Offline Scientific Intelligence Platform
Supports .iq and .npz • chemistry • physics • forensics • SDR (RX-only)
Type: help | status | forensic device | exit
══════════════════════════════════════════════════════════════
> 
```

### الأوامر المتاحة

```
> help

Available commands:
  status              - عرض الحالة
  sdr status          - حالة أجهزة SDR
  forensic device     - تحليل جهاز
  chemical-rf nmr     - تحليل NMR
  history             - سجل الأوامر
  exit                - خروج
```

### جلسة عملية مثال

```
> status
{
  "cli": "online",
  "mode": "offline-deterministic",
  "hardware": "not-opened",
  "network": "disabled",
  "rf_transmit": "disabled"
}

> sdr status
{
  "available_devices": {"rtl-sdr": [{"available": true, "device_index": 0}]},
  "receive_only": true
}

> history
1: status
2: sdr status

> exit
✓ Session closed safely.
```

---

## حل الأخطاء البرمجية

### خطأ 1: ملف الالتقاط غير موجود

```
FileNotFoundError: Capture file not found: capture.npz
```

**الحل:**
```bash
# تحقق من المسار
ls -la capture.npz

# أنشئ ملف التقاط جديد
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 2400000 \
  --duration 5 \
  --output capture.npz
```

---

### خطأ 2: صيغة ملف غير مدعومة

```
ValueError: Unsupported format: .wav. Use .npz or .iq files.
```

**الحل:**
```bash
# تحويل الملف إلى NPZ
vulture iq convert input.iq output.npz
```

---

### خطأ 3: معدل العينات غير محدد

```
ValueError: Missing sample-rate metadata for IQ file: capture.iq
```

**الحل:**
```bash
# أضف ملف JSON بجوار ملف IQ
# capture.iq.json
{
  "sample_rate": 2400000
}
```

---

### خطأ 4: جهاز SDR غير متصل

```
RuntimeError: No RTL-SDR devices found
```

**الحل:**
```bash
# تحقق من الاتصال
lsusb | grep RTL

# أو استخدم ملف التقاط موجود
vulture forensic device \
  --input existing_capture.npz \
  --case-id C-001 \
  --subject device-01 \
  --frequency-hz 433920000
```

---

### خطأ 5: خطأ الترجمة JSON

```
json.JSONDecodeError: Expecting value: line 1 column 1
```

**الحل:**
```bash
# تحقق من صيغة JSON
# جرّب:
vulture forensic chemistry \
  --case-id C-001 \
  --subject sample \
  --compounds-json '[{"name":"lead","concentration_ppm":2000}]'

# تأكد من علامات الاقتباس
```

---

### خطأ 6: سعة بطارية منخفضة أثناء الالتقاط

**الحل:**
```bash
# قلل المدة أو معدل العينات
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 1200000 \
  --duration 3 \
  --output short_capture.npz
```

---

## أمثلة متقدمة

### دورة عمل كاملة: تقييم أمان الجهاز

#### الخطوة 1: الالتقاط

```bash
vulture sdr capture \
  --device rtl-sdr \
  --frequency-hz 433920000 \
  --sample-rate 2400000 \
  --gain-db 20 \
  --duration 10 \
  --output device_capture.npz
```

#### الخطوة 2: التحليل السريع

```bash
vulture forensic device \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000
```

#### الخطوة 3: التقرير الشامل

```bash
vulture forensic report \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000 \
  --output final_report.json \
  --format json
```

#### الخطوة 4: عرض HTML

```bash
vulture forensic report \
  --input device_capture.npz \
  --case-id CASE-2026-001 \
  --subject mystery-device \
  --frequency-hz 433920000 \
  --output final_report.html \
  --format html
```

---

### استخدام المكتبة البايثون

```python
from vulture.forensic_analyzer import ForensicAnalyzer
import numpy as np

# تحميل البيانات
data = np.load('capture.npz')
samples = data['iq']
sample_rate = float(data['sample_rate'])

# إنشاء محلل جنائي
analyzer = ForensicAnalyzer('CASE-001', 'device-01')

# تحليل الالتقاط
analysis = analyzer.analyze_iq_capture(samples, sample_rate, 433920000)

# الحصول على النتائج
print(f"Score: {analysis.compromise_score}/100")
print(f"Status: {'COMPROMISED' if analysis.is_compromised else 'SAFE'}")
print(f"Indicators: {[i.value for i in analysis.compromise_indicators]}")

# إخراج JSON
print(analysis.to_json())

# إخراج نصي
print(analysis.to_text())
```

---

## الملخص

| المجال | الأوامر | الوظيفة |
|--------|--------|--------|
| **SDR** | status, info, capture, scan | استقبال وتسجيل إشارات RF |
| **الجنائي** | device, report, physics, chemistry, math, protocol | تحليل شامل للأجهزة |
| **الكيميائي-RF** | nmr, material, physics | تحليل الخصائص المادية |
| **RF-DNA** | simulate, fingerprint, dashboard, report | بصمات الأجهزة الفريدة |
| **التفاعلي** | --interactive | وضع سطر الأوامر التفاعلي |

---

## المراجع

- 📖 [VULTURE_COMPLETE_CLI_COMMANDS.md](docs/VULTURE_COMPLETE_CLI_COMMANDS.md)
- 🔧 [SDR_IQ_COMPLETE_GUIDE.md](docs/SDR_IQ_COMPLETE_GUIDE.md)
- 📚 [README.md](README.md)
- 🎯 [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)

---

**آخر تحديث:** 2026-10-09  
**الإصدار:** 1.0.0  
**الحالة:** ✅ مكتمل وقيد الاستخدام
