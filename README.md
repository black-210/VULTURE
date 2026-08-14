# TERFALCOM - Integrated DSP & ML Framework

## 📡 Overview
TERFALCOM (Telecom RF Analysis & ML Framework) is a comprehensive, production-ready framework combining:
- **RF Fingerprinting**: Signal processing + ML-based radio frequency classification
- **Visual Flowgraph Editor**: PyQt6 drag-and-drop DSP block orchestration
- **Model Hub**: Secure local ONNX model repository with verification
- **AI Orchestration**: LLM integration with safe execution hooks

## 🏗️ Project Structure

```
TERFALCOM/
├── rf_fingerprinting/          # RF signal classification framework
│   ├── __init__.py
│   ├── feature_extraction.py   # IQ data feature extraction
│   ├── preprocessing.py        # Signal preprocessing & normalization
│   ├── clustering.py           # K-means, DBSCAN clustering
│   ├── classifier.py           # SVM, Random Forest, Neural Net classifiers
│   ├── models/                 # Trained models storage
│   └── tests/
│       ├── test_feature_extraction.py
│       ├── test_preprocessing.py
│       ├── test_clustering.py
│       └── test_classifier.py
│
├── flowgraph_editor/           # PyQt6 Visual Editor
│   ├── __init__.py
│   ├── ui/
│   │   ├── main_window.py      # Main application window
│   │   ├── canvas.py           # Drag-drop canvas
│   │   ├── block_library.py    # DSP block catalog
│   │   └── styles.qss          # Qt stylesheet
│   ├── runtime/
│   │   ├── block.py            # Base DSP block class
│   │   ├── graph.py            # Execution graph
│   │   └── binding.py          # Runtime binding to DSP operations
│   └── tests/
│       ├── test_canvas.py
│       ├── test_block.py
│       └── test_graph.py
│
├── model_hub/                  # Model Repository & Management
│   ├── __init__.py
│   ├── repository.py           # Local model storage/retrieval
│   ├── onnx_loader.py          # ONNX model loading & inference
│   ├── verification.py         # Model signature verification
│   ├── models/                 # Model storage directory
│   └── tests/
│       ├── test_repository.py
│       ├── test_onnx_loader.py
│       └── test_verification.py
│
├── ai_orchestration/           # LLM Integration & Orchestration
│   ├── __init__.py
│   ├── adapters/
│   │   ├── __init__.py
│   │   ├── base_adapter.py     # Abstract LLM adapter interface
│   │   ├── openai_adapter.py   # OpenAI/ChatGPT implementation
│   │   ├── local_adapter.py    # Local LLM (Ollama, etc.)
│   │   └── mock_adapter.py     # Testing adapter
│   ├── execution.py            # Safe execution hooks & sandboxing
│   ├── prompts.py              # Prompt templates & management
│   └── tests/
│       ├── test_adapters.py
│       ├── test_execution.py
│       └── test_prompts.py
│
├── integration/                # Cross-module integration
│   ├── __init__.py
│   ├── pipeline.py             # End-to-end pipeline orchestration
│   └── tests/
│       └── test_pipeline.py
│
├── utils/                      # Shared utilities
│   ├── __init__.py
│   ├── config.py               # Configuration management
│   ├── logging.py              # Logging setup
│   └── validation.py           # Input validation
│
├── examples/                   # Usage examples
│   ├── rf_fingerprinting_demo.py
│   ├── flowgraph_demo.py
│   ├── model_hub_demo.py
│   └── ai_orchestration_demo.py
│
├── requirements.txt            # Python dependencies
├── setup.py                    # Package setup
├── pytest.ini                  # Pytest configuration
├── .gitignore
└── LICENSE

```

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/black-cyber-falcon/TERFALCOM.git
cd TERFALCOM
pip install -r requirements.txt
```

### Run Tests
```bash
pytest -v
```

### Launch Visual Editor
```bash
python -m flowgraph_editor.ui.main_window
```

## 📦 Core Components

### 1️⃣ RF Fingerprinting
Feature extraction from IQ data → Dimensionality reduction → Clustering → Classification

### 2️⃣ Visual Flowgraph Editor
Drag-drop PyQt6 canvas connecting DSP blocks with real-time signal flow visualization

### 3️⃣ Model Hub
Centralized ONNX model management with cryptographic verification and versioning

### 4️⃣ AI Orchestration
LLM adapter framework enabling safe integration with OpenAI, local models, and custom providers

## 📖 Documentation
Each module includes comprehensive docstrings and examples.

## 📝 License
MIT License - See LICENSE file

---

**Status**: 🟢 MVP Development in Progress
