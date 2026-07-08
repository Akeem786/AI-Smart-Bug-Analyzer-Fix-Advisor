# AI Smart Bug Analyzer & Fix Advisor

An AI-powered web application that allows users to submit bug reports, upload log/PDF/TXT files, extract file contents, and analyze software defects using FastAPI and React.

## Features

- Bug Report Submission
- File Upload Support (.txt, .log, .pdf)
- Automatic File Parsing
- REST API using FastAPI
- React Frontend
- Modular Project Structure
- Ready for AI/RAG Integration

## Tech Stack

### Frontend
- React.js
- Axios
- CSS

### Backend
- FastAPI
- Python
- PyPDF
- Uvicorn

## Project Structure

```
AI-Smart-Bug-Analyzer-Fix-Advisor
│
├── backend
│   ├── routes
│   ├── services
│   ├── uploads
│   └── main.py
│
├── frontend
│   ├── src
│   ├── public
│   └── package.json
│
├── docs
├── datasets
├── screenshots
├── requirements.txt
└── README.md
```

## Installation

### Clone Repository

```bash
git clone https://github.com/Snehakhatry91/AI-Smart-Bug-Analyzer-Fix-Advisor
```

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /submit | Submit Bug Report |
| POST | /analyze | Analyze Bug |
| GET | /health | Health Check |

## Future Enhancements

- AI Root Cause Analysis
- LLM Integration
- Vector Database
- RAG Pipeline
- Fix Recommendation Engine

## Author

**Sneha Khatry**

B.Tech CSE (CC)Student

CV Raman Global University

GitHub: https://github.com/Snehakhatry91