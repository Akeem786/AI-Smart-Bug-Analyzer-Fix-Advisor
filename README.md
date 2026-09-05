# 🛡️AI-Smart-Bug-Analyzer-Fix-Advisor


<div align="center">

[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18.0+-61DAFB.svg?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org)
[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![Vite](https://img.shields.io/badge/Vite-5.0+-646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)](https://vitejs.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=for-the-badge)](CONTRIBUTING.md)

**An autonomous multi-agent intelligence platform for software defect triage, stack trace & server log diagnostics, root cause timeline reconstruction, duplicate bug detection, and automated code patch generation.**

[Explore Features](#-key-features) • [System Architecture](#-multi-agent-architecture) • [Getting Started](#-getting-started) • [API Reference](#-api-endpoints) • [License](#-license)

</div>

---

## 📌 Overview

Debugging modern distributed systems is challenging: stack traces are noisy, logs span thousands of lines, and locating past duplicate incidents takes hours.

**AI Log Diagnostic & Automated Remediation System** automates the entire debugging lifecycle using a specialized **Multi-Agent AI Pipeline**. Simply paste a stack trace or upload a raw log/PDF file, and the platform delivers:
- **Instant Triage**: Severity rating (P0–P3), Risk Index (0–100), and SLA resolution target.
- **Log Parsing**: Extracted stack frames, affected files, line numbers, and error signatures.
- **Root Cause Analysis**: Probable failure mechanism, affected layers, blast radius, and an execution timeline.
- **Automated Remediation**: Unified/Split diff view with production-ready defensive code patches and downloadable `.patch` files.
- **Duplicate Detection**: Retrieval-Augmented Generation (RAG) lookup against known defect repositories.

---

## ✨ Key Features

### 🤖 1. Multi-Agent AI Pipeline
- **Triage Agent**: Evaluates defect severity, business risk, and assigns strict SLA response targets.
- **Log Analysis Agent**: Parses unstructured server logs, isolates stack frames, and summarizes exception signatures.
- **Root Cause Agent**: Synthesizes fault triggers, isolates failure blast radius, and reconstructs execution timelines.
- **Duplicate Agent**: Compares defects against indexed vector repositories to locate matching resolved incidents.
- **Remediation Agent**: Recommends defensive programming fixes, structural prevention advice, and generates standard unified diffs.

### 💻 2. Interactive Visual Code Diff Viewer
- **Unified Diff Mode**: Standard Git-style syntax highlighting (+ added, - removed).
- **Split View Mode**: Side-by-side comparison of buggy code vs. remediated code.
- **Clean Fix View**: One-click view of the final production-ready code.
- **Export & Download**: One-click `.patch` file download and clipboard copy.

### 📄 3. Universal Log & Document Parsing
- Ingests `.log`, `.txt`, and `.pdf` documents directly via drag-and-drop.
- Integrated PDF parser powered by `PyPDF` with multi-encoding fallbacks (`utf-8`, `latin-1`, `cp1252`).
- Safe truncation guardrails for oversized log files.

### ⚡ 4. Enterprise Developer Experience
- **Interactive Presets**: Quick-load sample defects (Java NullPointerException, Database Pool Exhaustion, React Undefined Map, Python OOM Worker Kill, CORS preflight failures).
- **Defect History**: Instant local cache of past triage sessions.
- **Real-Time Backend Health Monitoring**: Live visual connection indicator communicating with FastAPI.

---

## 🏗️ Multi-Agent Architecture

```text
                                   [ User Input / Log Upload ]
                                                │
                                    ┌───────────┴───────────┐
                                    ▼                       ▼
                              Raw Stack Trace       .log / .pdf Parser
                                    │                       │
                                    └───────────┬───────────┘
                                                │
                                                ▼
                                    ┌───────────────────────┐
                                    │    FastAPI Gateway    │
                                    └───────────┬───────────┘
                                                │
                      ┌─────────────────────────┼─────────────────────────┐
                      ▼                         ▼                         ▼
            ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
            │   Triage Agent   │      │Log Analysis Agent│      │ Root Cause Agent │
            │  • Severity/Risk │      │ • Stack Frames   │      │ • Timeline Graph │
            │  • SLA Target    │      │ • Exceptions     │      │ • Blast Radius   │
            └──────────────────┘      └──────────────────┘      └──────────────────┘
                      │                         │                         │
                      └─────────────────────────┼─────────────────────────┘
                                                ▼
                               ┌─────────────────────────────────┐
                               │   Knowledge Base / RAG Agent    │
                               │   • Similar Bug Similarity      │
                               │   • Past Resolution Retrieval   │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │        Remediation Agent        │
                               │   • Unified & Split Diff View   │
                               │   • Downloadable .patch File    │
                               │   • Preventive Action Checklist │
                               └────────────────┬────────────────┘
                                                │
                                                ▼
                               ┌─────────────────────────────────┐
                               │    React Executive Dashboard    │
                               └─────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Description |
| :--- | :--- | :--- |
| **Frontend Framework** | **React.js 18** | High-performance, component-based user interface |
| **Frontend Bundler** | **Vite** | Next-generation frontend tooling and fast HMR |
| **HTTP Client** | **Axios** | Async API communication with backend |
| **Backend Framework** | **FastAPI** | Modern, asynchronous high-performance Python REST API |
| **Server Engine** | **Uvicorn** | Lightning-fast ASGI web server implementation |
| **Document Processing** | **PyPDF** | Binary PDF stream parsing and text extraction |
| **Data Validation** | **Pydantic v2** | Strict payload typing and schema enforcement |
| **Retrieval Engine** | **RAG Vector Mock** | Substring and contextual similarity matcher |

---

## 📁 Project Structure

```text
Ai-log-diagnostic-and-automated-remediation-system
├── backend/
│   ├── agents/                   # Specialized AI Analysis Agents
│   │   ├── triage_agent.py       # Severity, priority, risk & SLA agent
│   │   ├── log_analysis_agent.py # Stack trace frame & error extractor
│   │   ├── root_cause_agent.py   # Failure mechanism & timeline generator
│   │   ├── duplicate_agent.py    # Past defect similarity finder
│   │   └── remediation_agent.py  # Code patch & diff generator
│   ├── rag/                      # Retrieval-Augmented Generation module
│   │   ├── retriever.py          # Similarity search engine
│   │   ├── ingest.py             # Knowledge base loader
│   │   └── chunking.py           # Document chunker
│   ├── routes/                   # FastAPI Endpoints
│   │   ├── analyze.py            # Primary defect analysis pipelines
│   │   ├── upload.py             # File upload and parsing route
│   │   └── health.py             # Server heartbeat check
│   ├── services/                 # Core backend services
│   │   └── file_parser.py        # Multi-encoding log & PDF parser
│   ├── uploads/                  # Temporary upload staging area
│   ├── main.py                   # FastAPI application entrypoint
│   └── requirements.txt          # Python dependencies
│
├── frontend/
│   ├── src/
│   │   ├── components/           # Modular React components
│   │   │   ├── AnalysisDashboard.jsx # Executive analysis & diagnostics view
│   │   │   ├── BugForm.jsx           # Defect submission, drag-and-drop, presets
│   │   │   ├── DiffViewer.jsx        # Unified & split code diff viewer
│   │   │   ├── ExecutionFlow.jsx     # Root cause timeline visualizer
│   │   │   └── Icons.jsx             # Feather-style SVG icons
│   │   ├── pages/
│   │   │   └── Home.jsx          # Main application page layout
│   │   ├── services/
│   │   │   └── api.js            # Axios client configuration
│   │   ├── App.jsx
│   │   └── index.css             # Glassmorphism dark-mode styling
│   ├── package.json
│   └── vite.config.js
│
├── datasets/
│   └── known_defects.json        # Historical defect repository for duplicate lookup
├── LICENSE
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.10+** (Tested on Python 3.11 & 3.12)
- **Node.js 18+** & **npm**

---

### 1. Clone the Repository
```bash
git clone https://github.com/Akeem786/Ai-log-diagnostic-and-automated-remediation-system.git
cd Ai-log-diagnostic-and-automated-remediation-system
```

---

### 2. Backend Setup
```bash
# Navigate to backend
cd backend

# (Optional) Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
> Backend will be running at **http://127.0.0.1:8000**  
> Interactive Swagger API docs available at **http://127.0.0.1:8000/docs**

---

### 3. Frontend Setup
Open a new terminal window:
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start Vite dev server
npm run dev
```
> Frontend web app will be running at **http://localhost:5173**

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Request Type |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | System health and readiness check | `None` |
| `POST` | `/submit-and-analyze` | Single-step log upload + multi-agent defect analysis | `multipart/form-data` |
| `POST` | `/analyze` | Run multi-agent pipeline on JSON payload | `application/json` |
| `POST` | `/submit` | Upload and parse file without immediate analysis | `multipart/form-data` |
| `GET` | `/docs` | Interactive Swagger API documentation | `None` |

### Sample Analysis Request (`/submit-and-analyze`)
```bash
curl -X POST "http://127.0.0.1:8000/submit-and-analyze" \
  -F "bug_report=java.lang.NullPointerException: Cannot invoke getRoles() because user is null" \
  -F "file=@sample_error.log"
```

---

## 🤝 Contributing

Contributions are warmly welcomed! If you'd like to improve the multi-agent pipelines, add LLM integrations, or enhance the dashboard UI:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for more information.

---

<div align="center">
  <sub>Built with ❤️ using FastAPI & React. Star ⭐ this repository if you find it helpful!</sub>
</div>
