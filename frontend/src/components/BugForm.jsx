import React, { useState, useRef, useEffect } from "react";
import api from "../services/api";
import {
  UploadCloudIcon,
  Trash2Icon,
  SparklesIcon,
  FileTextIcon,
  AlertTriangleIcon,
  CheckCircleIcon
} from "./Icons";

const CATEGORIZED_PRESETS = [
  {
    category: "Java",
    badgeColor: "#f59e0b",
    label: "NullPointerException",
    text: `java.lang.NullPointerException: Cannot invoke 'com.example.User.getRoles()' because 'user' is null
    at com.example.service.AuthService.validateToken(AuthService.java:42)
    at com.example.controller.AuthController.login(AuthController.java:28)
Triggered when user session expires and incoming JWT payload fails DB lookup.`
  },
  {
    category: "Database",
    badgeColor: "#ef4444",
    label: "DB Pool Exhausted",
    text: `sqlalchemy.exc.TimeoutError: QueuePool limit of size 10 overflow 10 reached, connection timed out, timeout 30.00
    at /app/database/connection.py:65 in acquire_connection
High concurrent API traffic during flash sale caused all DB handles to deadlock.`
  },
  {
    category: "React",
    badgeColor: "#06b6d4",
    label: "Undefined .map()",
    text: `TypeError: Cannot read properties of undefined (reading 'map')
    at UserList.render (UserList.jsx:18:24)
    at renderWithHooks (react-dom.js:14985:18)
Component renders before asynchronous user list API promise resolves.`
  },
  {
    category: "Python",
    badgeColor: "#10b981",
    label: "OOM Worker Kill",
    text: `Worker process terminated by Linux kernel OOM-killer (SIGKILL).
Worker memory exceeded container cgroup limit of 2048MB during PDF batch aggregation export.`
  },
  {
    category: "API",
    badgeColor: "#a855f7",
    label: "CORS Blocked",
    text: `Access to XMLHttpRequest at 'http://127.0.0.1:8000/analyze' from origin 'http://localhost:5173' has been blocked by CORS policy:
Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present.`
  }
];

export default function BugForm({ onAnalysisSuccess, onStartAnalysis, isAnalyzing }) {
  const [bugReport, setBugReport] = useState("");
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [loadingStep, setLoadingStep] = useState("");
  const [recentHistory, setRecentHistory] = useState([]);
  const fileInputRef = useRef(null);

  // Load history from localStorage
  useEffect(() => {
    try {
      const saved = localStorage.getItem("defect_analyzer_history");
      if (saved) {
        setRecentHistory(JSON.parse(saved));
      }
    } catch {
      // ignore
    }
  }, []);

  const saveToHistory = (title, report, result) => {
    const item = {
      id: Date.now(),
      title: title || report.substring(0, 45) + "...",
      timestamp: new Date().toLocaleTimeString(),
      report,
      result
    };
    const updated = [item, ...recentHistory.filter((h) => h.report !== report)].slice(0, 5);
    setRecentHistory(updated);
    try {
      localStorage.setItem("defect_analyzer_history", JSON.stringify(updated));
    } catch {
      // ignore
    }
  };

  const applyPreset = (preset) => {
    setBugReport(preset.text);
    setErrorMessage("");
  };

  const applyHistoryItem = (item) => {
    setBugReport(item.report);
    if (item.result) {
      onAnalysisSuccess(item.result);
    }
    setErrorMessage("");
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (selectedFile) => {
    const validExtensions = [".txt", ".log", ".pdf"];
    const ext = selectedFile.name.substring(selectedFile.name.lastIndexOf(".")).toLowerCase();
    if (!validExtensions.includes(ext)) {
      setErrorMessage("Please upload a supported format: .txt, .log, or .pdf");
      return;
    }
    setFile(selectedFile);
    setErrorMessage("");
  };

  const removeFile = () => {
    setFile(null);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const clearForm = () => {
    setBugReport("");
    removeFile();
    setErrorMessage("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!bugReport.trim() && !file) {
      setErrorMessage("Please enter a stack trace / description or attach a log file.");
      return;
    }

    setErrorMessage("");
    onStartAnalysis();

    const steps = [
      "Parsing log file and extracting metadata...",
      "Isolating stack frames and exception signatures...",
      "Evaluating severity & SLA response targets...",
      "Searching vector repository for similar bugs...",
      "Synthesizing root cause & generating defensive code patch..."
    ];

    let stepIndex = 0;
    setLoadingStep(steps[0]);
    const stepInterval = setInterval(() => {
      stepIndex = (stepIndex + 1) % steps.length;
      setLoadingStep(steps[stepIndex]);
    }, 550);

    const formData = new FormData();
    formData.append("bug_report", bugReport || "Attached file analysis");
    if (file) {
      formData.append("file", file);
    }

    try {
      const response = await api.post("/submit-and-analyze", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      clearInterval(stepInterval);
      onAnalysisSuccess(response.data);

      const title = response.data?.triage?.impact_summary || response.data?.log_analysis?.error_type;
      saveToHistory(title, bugReport || file.name, response.data);
    } catch (err) {
      clearInterval(stepInterval);
      console.error("Submission failed:", err);
      if (err.response) {
        setErrorMessage(`Server Error (${err.response.status}): ${err.response.data?.detail || "Analysis request failed."}`);
      } else if (err.request) {
        setErrorMessage("Cannot connect to FastAPI backend on http://127.0.0.1:8000. Ensure the server is running.");
      } else {
        setErrorMessage(err.message || "An unexpected error occurred.");
      }
      onAnalysisSuccess(null);
    }
  };

  const lineCount = bugReport ? bugReport.split("\n").length : 0;
  const charCount = bugReport.length;

  return (
    <div className="glass-card">
      <div className="card-header">
        <div className="card-title-group">
          <div className="card-icon-box">
            <SparklesIcon size={20} />
          </div>
          <div>
            <h2 className="card-title">Defect Submission & Parsing</h2>
            <p className="card-subtitle">
              Input software stack traces or upload log archives
            </p>
          </div>
        </div>

        {recentHistory.length > 0 && (
          <span style={{ fontSize: "11px", color: "#94a3b8", background: "rgba(255,255,255,0.04)", padding: "4px 8px", borderRadius: "4px" }}>
            {recentHistory.length} in history
          </span>
        )}
      </div>

      {/* Preset Quick-Load Bar */}
      <div className="presets-section">
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: "8px" }}>
          <span className="presets-label" style={{ margin: 0 }}>
            <SparklesIcon size={12} />
            Quick Presets
          </span>
          {recentHistory.length > 0 && (
            <div style={{ display: "flex", gap: "6px", alignItems: "center" }}>
              <span style={{ fontSize: "11px", color: "#64748b" }}>History:</span>
              {recentHistory.slice(0, 2).map((item) => (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => applyHistoryItem(item)}
                  style={{
                    background: "rgba(139, 92, 246, 0.1)",
                    border: "1px solid rgba(139, 92, 246, 0.25)",
                    color: "#c4b5fd",
                    fontSize: "11px",
                    padding: "2px 8px",
                    borderRadius: "4px",
                    cursor: "pointer"
                  }}
                  title={item.title}
                >
                  {item.title.substring(0, 16)}...
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="preset-chips-wrap">
          {CATEGORIZED_PRESETS.map((p, idx) => (
            <button
              key={idx}
              type="button"
              className="preset-chip"
              onClick={() => applyPreset(p)}
            >
              <span
                className="preset-dot"
                style={{ backgroundColor: p.badgeColor }}
              />
              <span className="preset-chip-category">{p.category}:</span>
              <span className="preset-chip-label">{p.label}</span>
            </button>
          ))}
        </div>
      </div>

      <form onSubmit={handleSubmit}>
        {/* Bug Text Area with clean text wrapping */}
        <div className="form-group">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "6px" }}>
            <label className="form-label" htmlFor="bug-report-input" style={{ margin: 0 }}>
              Bug Narrative / Raw Stack Trace
            </label>
            <span style={{ fontSize: "10.5px", color: "#64748b", fontFamily: "var(--font-mono)" }}>
              {lineCount} lines • {charCount} chars
            </span>
          </div>

          <textarea
            id="bug-report-input"
            className="bug-textarea"
            rows="8"
            placeholder="Paste complete stack trace, exception log, or failure narrative..."
            value={bugReport}
            onChange={(e) => setBugReport(e.target.value)}
            spellCheck="false"
          />
        </div>

        {/* Drag & Drop Upload Zone */}
        <div className="form-group">
          <label className="form-label">Attach File (.txt, .log, .pdf)</label>
          <div
            className={`dropzone-container ${dragActive ? "active" : ""}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
            onClick={() => fileInputRef.current?.click()}
          >
            <input
              ref={fileInputRef}
              type="file"
              accept=".txt,.log,.pdf"
              style={{ display: "none" }}
              onChange={handleFileChange}
            />
            <div className="dropzone-icon">
              <UploadCloudIcon size={30} />
            </div>
            <div className="dropzone-text">
              Drop log, text, or PDF file here, or click to browse
            </div>
            <div className="dropzone-hint">
              Supports server .log files, exception reports (.txt), and architecture PDFs
            </div>
          </div>

          {file && (
            <div className="file-pill">
              <div className="file-info">
                <FileTextIcon size={16} />
                <span>{file.name}</span>
                <span style={{ fontSize: "11px", color: "#94a3b8" }}>
                  ({(file.size / 1024).toFixed(1)} KB)
                </span>
              </div>
              <button
                type="button"
                className="remove-file-btn"
                onClick={removeFile}
                title="Remove file"
              >
                <Trash2Icon size={16} />
              </button>
            </div>
          )}
        </div>

        {/* Error Banner */}
        {errorMessage && (
          <div style={{
            background: "rgba(239, 68, 68, 0.15)",
            border: "1px solid rgba(239, 68, 68, 0.4)",
            color: "#fca5a5",
            borderRadius: "8px",
            padding: "12px 14px",
            fontSize: "13px",
            marginBottom: "16px",
            display: "flex",
            alignItems: "center",
            gap: "10px"
          }}>
            <AlertTriangleIcon size={16} />
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Action Buttons */}
        <div className="form-actions-row">
          <button
            type="submit"
            className="btn-primary"
            disabled={isAnalyzing}
          >
            <SparklesIcon size={18} />
            <span>{isAnalyzing ? "Analyzing Defect..." : "Analyze Defect"}</span>
          </button>

          <button
            type="button"
            className="btn-secondary"
            onClick={clearForm}
            disabled={isAnalyzing}
          >
            Clear
          </button>
        </div>
      </form>

      {/* Progressive Step Progress */}
      {isAnalyzing && (
        <div className="analyzing-box">
          <div className="spinner"></div>
          <div className="analyzing-step-text">{loadingStep}</div>
          <div className="analyzing-subtext">Executing multi-agent defect intelligence pipeline...</div>
        </div>
      )}
    </div>
  );
}