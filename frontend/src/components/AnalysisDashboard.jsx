import React, { useState } from "react";
import DiffViewer from "./DiffViewer";
import ExecutionFlow from "./ExecutionFlow";
import {
  ShieldCheckIcon,
  AlertTriangleIcon,
  ActivityIcon,
  TerminalIcon,
  CpuIcon,
  SparklesIcon,
  FileTextIcon,
  CopyIcon,
  CheckIcon
} from "./Icons";

export default function AnalysisDashboard({ analysisData, uploadedFile, fileContent }) {
  const [activeTab, setActiveTab] = useState("remediation");
  const [copiedReport, setCopiedReport] = useState(false);

  if (!analysisData) {
    return (
      <div className="glass-card">
        <div className="empty-placeholder">
          <div className="empty-icon">
            <SparklesIcon size={48} />
          </div>
          <h3 className="empty-title">AI Analysis Engine Idle</h3>
          <p className="empty-desc">
            Submit a defect narrative or select a preset to generate automated triage,
            visual code diffs, root-cause diagnostics, and fix advice.
          </p>
        </div>
      </div>
    );
  }

  const { triage, log_analysis, root_cause, duplicate_bugs, remediation } = analysisData;

  const getSeverityBadgeClass = (sev) => {
    switch (sev?.toLowerCase()) {
      case "critical":
        return "badge-critical";
      case "high":
        return "badge-high";
      case "medium":
        return "badge-medium";
      case "low":
        return "badge-low";
      default:
        return "badge-medium";
    }
  };

  const copyFullReport = () => {
    const reportStr = JSON.stringify(analysisData, null, 2);
    navigator.clipboard.writeText(reportStr);
    setCopiedReport(true);
    setTimeout(() => setCopiedReport(false), 2000);
  };

  return (
    <div className="results-container">
      {/* Top Metrics Row */}
      <div className="triage-metrics-row">
        <div className="metric-card">
          <span className="metric-label">Severity</span>
          <div className="metric-val-wrap">
            <span className={`badge ${getSeverityBadgeClass(triage?.severity)}`}>
              <AlertTriangleIcon size={13} />
              {triage?.severity || "Medium"}
            </span>
          </div>
        </div>

        <div className="metric-card">
          <span className="metric-label">Priority SLA</span>
          <div className="metric-val-wrap">
            <span className={`badge ${getSeverityBadgeClass(triage?.severity)}`}>
              {triage?.priority || "P2"}
            </span>
          </div>
        </div>

        <div className="metric-card">
          <span className="metric-label">Risk Index</span>
          <div className="metric-val-wrap">
            <div className="risk-progress-bar-wrap">
              <div
                className={`risk-progress-bar-fill ${
                  (triage?.risk_score || 50) >= 80 ? "critical" : (triage?.risk_score || 50) >= 60 ? "high" : "medium"
                }`}
                style={{ width: `${triage?.risk_score || 50}%` }}
              />
            </div>
            <span style={{ fontSize: "14px", fontWeight: "700", color: "#f8fafc" }}>
              {triage?.risk_score || 50}/100
            </span>
          </div>
        </div>

        <div className="metric-card">
          <span className="metric-label">Defect Domain</span>
          <div className="metric-val-wrap">
            <span style={{ fontSize: "13px", fontWeight: "600", color: "#c4b5fd" }}>
              {triage?.category || "General Logic"}
            </span>
          </div>
        </div>
      </div>

      {/* Main Analysis Container */}
      <div className="glass-card">
        <div className="card-header">
          <div className="card-title-group">
            <div className="card-icon-box">
              <CpuIcon size={20} />
            </div>
            <div>
              <h2 className="card-title">Defect Diagnostics & Advisor</h2>
              <p className="card-subtitle">
                Multi-agent analysis, visual diff remediation & root cause graph
              </p>
            </div>
          </div>

          <button className="btn-copy" onClick={copyFullReport} title="Export analysis JSON">
            {copiedReport ? <CheckIcon size={14} /> : <CopyIcon size={14} />}
            <span>{copiedReport ? "Copied" : "Export JSON"}</span>
          </button>
        </div>

        {/* Tab Navigation */}
        <div className="tabs-nav">
          <button
            className={`tab-btn ${activeTab === "remediation" ? "active" : ""}`}
            onClick={() => setActiveTab("remediation")}
          >
            <ShieldCheckIcon size={15} />
            Fix Advisor & Diff
          </button>

          <button
            className={`tab-btn ${activeTab === "rootcause" ? "active" : ""}`}
            onClick={() => setActiveTab("rootcause")}
          >
            <CpuIcon size={15} />
            Root Cause & Timeline
          </button>

          <button
            className={`tab-btn ${activeTab === "logs" ? "active" : ""}`}
            onClick={() => setActiveTab("logs")}
          >
            <TerminalIcon size={15} />
            Log Diagnostics
          </button>

          <button
            className={`tab-btn ${activeTab === "triage" ? "active" : ""}`}
            onClick={() => setActiveTab("triage")}
          >
            <ActivityIcon size={15} />
            Triage & SLA
          </button>

          <button
            className={`tab-btn ${activeTab === "duplicates" ? "active" : ""}`}
            onClick={() => setActiveTab("duplicates")}
          >
            <SparklesIcon size={15} />
            Similar Bugs ({duplicate_bugs?.length || 0})
          </button>

          {fileContent && (
            <button
              className={`tab-btn ${activeTab === "file" ? "active" : ""}`}
              onClick={() => setActiveTab("file")}
            >
              <FileTextIcon size={15} />
              Parsed File
            </button>
          )}
        </div>

        {/* Tab Panels */}
        <div className="tab-content" style={{ marginTop: "18px" }}>
          {/* TAB: FIX ADVISOR & DIFF */}
          {activeTab === "remediation" && (
            <div>
              <div className="section-block">
                <h4 className="section-subtitle">
                  <ShieldCheckIcon size={16} />
                  Remediation Strategy
                </h4>
                <p style={{ fontSize: "14px", color: "#f8fafc", fontWeight: "600", marginBottom: "14px" }}>
                  {remediation?.recommendation}
                </p>

                {/* Diff Viewer Component */}
                <DiffViewer remediation={remediation} />

                {/* Actionable Steps */}
                {remediation?.remediation_steps?.length > 0 && (
                  <div style={{ marginTop: "20px" }}>
                    <h5 style={{ fontSize: "12px", color: "#94a3b8", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "10px" }}>
                      Implementation Action Steps
                    </h5>
                    <ul className="steps-list">
                      {remediation.remediation_steps.map((step, idx) => (
                        <li key={idx} className="step-item">
                          <span className="step-num">{idx + 1}</span>
                          <span>{step}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}

                {/* Preventive Actions */}
                {remediation?.preventive_actions?.length > 0 && (
                  <div style={{ marginTop: "18px", padding: "12px 16px", background: "rgba(255,255,255,0.02)", borderRadius: "8px", border: "1px solid var(--border-subtle)" }}>
                    <h5 style={{ fontSize: "12px", color: "#c4b5fd", textTransform: "uppercase", letterSpacing: "0.5px", marginBottom: "8px" }}>
                      Long-Term Preventive Measures
                    </h5>
                    <ul style={{ paddingLeft: "18px", color: "#94a3b8", fontSize: "13px", lineHeight: "1.7" }}>
                      {remediation.preventive_actions.map((act, i) => (
                        <li key={i}>{act}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          )}

          {/* TAB: ROOT CAUSE & TIMELINE */}
          {activeTab === "rootcause" && (
            <div>
              <ExecutionFlow rootCause={root_cause} />
            </div>
          )}

          {/* TAB: LOG DIAGNOSTICS */}
          {activeTab === "logs" && (
            <div>
              <div className="section-block">
                <h4 className="section-subtitle">
                  <TerminalIcon size={16} />
                  Detected Error Signatures
                </h4>
                <p style={{ fontSize: "13px", color: "#94a3b8", marginBottom: "12px" }}>
                  {log_analysis?.summary}
                </p>
                {log_analysis?.detected_exceptions?.length > 0 && (
                  <div style={{ display: "flex", gap: "8px", flexWrap: "wrap", marginBottom: "18px" }}>
                    {log_analysis.detected_exceptions.map((exc, i) => (
                      <span key={i} className="badge badge-critical" style={{ fontFamily: "monospace", fontSize: "12px" }}>
                        {exc}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {log_analysis?.stack_frames?.length > 0 ? (
                <div className="section-block">
                  <h4 className="section-subtitle">Parsed Stack Trace Call Frames</h4>
                  <div className="frames-list">
                    {log_analysis.stack_frames.map((frame, idx) => (
                      <div key={idx} className="frame-item">
                        <span className="frame-file">
                          {frame.file} : <strong style={{ color: "#38bdf8" }}>line {frame.line}</strong>
                          {frame.function !== "N/A" && (
                            <span style={{ color: "#94a3b8", marginLeft: "6px" }}>in {frame.function}()</span>
                          )}
                        </span>
                        <span className="frame-badge">{frame.type}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ) : (
                <p style={{ fontSize: "13px", color: "#64748b" }}>
                  No explicit stack frames detected in log text.
                </p>
              )}
            </div>
          )}

          {/* TAB: TRIAGE & SLA */}
          {activeTab === "triage" && (
            <div>
              <div className="section-block">
                <h4 className="section-subtitle">
                  <ActivityIcon size={16} />
                  Operational Impact Summary
                </h4>
                <p style={{ fontSize: "14px", color: "#e2e8f0", marginBottom: "14px" }}>
                  {triage?.impact_summary || "Defect triaged."}
                </p>
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "12px", fontSize: "13px" }}>
                  <div style={{ background: "var(--bg-surface)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border-subtle)" }}>
                    <span style={{ color: "#64748b", display: "block", marginBottom: "4px" }}>Target Resolution SLA</span>
                    <strong style={{ color: "#f1f5f9", fontSize: "14px" }}>{triage?.sla_target}</strong>
                  </div>
                  <div style={{ background: "var(--bg-surface)", padding: "12px", borderRadius: "8px", border: "1px solid var(--border-subtle)" }}>
                    <span style={{ color: "#64748b", display: "block", marginBottom: "4px" }}>Classification Domain</span>
                    <strong style={{ color: "#38bdf8", fontSize: "14px" }}>{triage?.category}</strong>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* TAB: SIMILAR BUGS */}
          {activeTab === "duplicates" && (
            <div>
              <div className="section-block">
                <h4 className="section-subtitle">
                  <SparklesIcon size={16} />
                  Knowledge Base & Duplicate Defect Candidates
                </h4>
                {duplicate_bugs && duplicate_bugs.length > 0 ? (
                  duplicate_bugs.map((bug, i) => (
                    <div key={i} className="dup-card">
                      <div className="dup-header">
                        <span className="dup-id">{bug.id} • {bug.component}</span>
                        <span className="dup-score">
                          {bug.similarity_score} Match
                        </span>
                      </div>
                      <h4 className="dup-title">{bug.title}</h4>
                      <p className="dup-desc">{bug.description}</p>
                      {bug.resolution && (
                        <div className="dup-fix">
                          <strong>Past Resolution:</strong> {bug.resolution}
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <p style={{ fontSize: "13px", color: "#64748b" }}>
                    No similar defects found in the knowledge repository.
                  </p>
                )}
              </div>
            </div>
          )}

          {/* TAB: PARSED FILE CONTENT */}
          {activeTab === "file" && fileContent && (
            <div>
              <div className="section-block">
                <div className="code-box">
                  <div className="code-header">
                    <span className="code-title">
                      Raw File Contents: {uploadedFile || "Uploaded File"} ({fileContent.length} chars)
                    </span>
                  </div>
                  <pre className="code-pre" style={{ maxHeight: "350px", overflowY: "auto", color: "#cbd5e1" }}>
                    {fileContent}
                  </pre>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
