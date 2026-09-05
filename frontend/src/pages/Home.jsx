import React, { useState, useEffect } from "react";
import BugForm from "../components/BugForm";
import AnalysisDashboard from "../components/AnalysisDashboard";
import api from "../services/api";
import { BugIcon, ActivityIcon, SparklesIcon } from "../components/Icons";

export default function Home() {
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [serverStatus, setServerStatus] = useState("checking"); // online, offline, checking

  const checkHealth = async () => {
    try {
      const res = await api.get("/health");
      if (res.data && res.data.status === "Healthy") {
        setServerStatus("online");
      } else {
        setServerStatus("offline");
      }
    } catch {
      setServerStatus("offline");
    }
  };

  useEffect(() => {
    checkHealth();
    const timer = setInterval(checkHealth, 15000);
    return () => clearInterval(timer);
  }, []);

  const handleStartAnalysis = () => {
    setIsAnalyzing(true);
  };

  const handleAnalysisSuccess = (data) => {
    setIsAnalyzing(false);
    if (data) {
      setAnalysisResult(data);
    }
  };

  return (
    <>
      {/* Top Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="brand-badge">
            <div className="logo-icon-box">
              <BugIcon size={24} />
            </div>
            <div>
              <div className="brand-title">
                AI Bug Analyzer
                <span className="brand-tag">v1.0 AI</span>
              </div>
            </div>
          </div>

          <div className="header-actions">
            <div className="server-status" title={`FastAPI Server: ${serverStatus}`}>
              <div
                className={`status-dot ${
                  serverStatus === "online" ? "online" : "offline"
                }`}
              />
              <span>
                {serverStatus === "online"
                  ? "FastAPI 8000 Ready"
                  : serverStatus === "checking"
                  ? "Checking Backend..."
                  : "Backend Offline"}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Container */}
      <main className="app-container">
        {/* Hero Section */}
        <section className="hero-banner">
          <div className="hero-pill">
            <SparklesIcon size={14} />
            <span>Autonomous Defect Triage & Remediation</span>
          </div>
          <h1 className="hero-title">
            AI Smart <span className="gradient-text">Bug Analyzer</span> & Fix Advisor
          </h1>
          <p className="hero-subtitle">
            Upload server logs, stack traces, or PDF bug reports. Our multi-agent intelligence
            engine classifies severity, identifies root causes, locates duplicate defects,
            and advises production-ready fixes.
          </p>
        </section>

        {/* Workspace Grid */}
        <div className="main-workspace-grid">
          {/* Submission Panel */}
          <div>
            <BugForm
              onStartAnalysis={handleStartAnalysis}
              onAnalysisSuccess={handleAnalysisSuccess}
              isAnalyzing={isAnalyzing}
            />
          </div>

          {/* Results Panel */}
          <div>
            <AnalysisDashboard
              analysisData={analysisResult}
              uploadedFile={analysisResult?.uploaded_file}
              fileContent={analysisResult?.file_content}
            />
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div style={{ display: "flex", justifyContent: "center", alignItems: "center", gap: "8px" }}>
          <span>AI Defect Analysis System • Powered by FastAPI & React</span>
        </div>
      </footer>
    </>
  );
}