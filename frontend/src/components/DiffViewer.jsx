import React, { useState } from "react";
import { CopyIcon, CheckIcon, FileTextIcon } from "./Icons";

export default function DiffViewer({ remediation }) {
  const [viewMode, setViewMode] = useState("diff"); // 'diff', 'split', 'fixed'
  const [copied, setCopied] = useState(false);
  const [copiedPatch, setCopiedPatch] = useState(false);

  if (!remediation) return null;

  const { target_file, before_code, after_code, diff_lines, patch_file_content } = remediation;

  const handleCopyCode = () => {
    navigator.clipboard.writeText(after_code || remediation.code_patch);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownloadPatch = () => {
    const blob = new Blob([patch_file_content || after_code], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${target_file || "defect_fix"}.patch`;
    a.click();
    URL.revokeObjectURL(url);
    setCopiedPatch(true);
    setTimeout(() => setCopiedPatch(false), 2500);
  };

  return (
    <div className="diff-viewer-wrapper">
      {/* Diff Toolbar */}
      <div className="diff-toolbar">
        <div className="diff-file-tag">
          <FileTextIcon size={14} />
          <span>{target_file || "patch.diff"}</span>
        </div>

        <div className="diff-actions-group">
          <div className="diff-mode-toggles">
            <button
              className={`mode-toggle-btn ${viewMode === "diff" ? "active" : ""}`}
              onClick={() => setViewMode("diff")}
            >
              Unified Diff
            </button>
            <button
              className={`mode-toggle-btn ${viewMode === "split" ? "active" : ""}`}
              onClick={() => setViewMode("split")}
            >
              Split View
            </button>
            <button
              className={`mode-toggle-btn ${viewMode === "fixed" ? "active" : ""}`}
              onClick={() => setViewMode("fixed")}
            >
              Clean Fix
            </button>
          </div>

          <button className="diff-btn-action" onClick={handleDownloadPatch} title="Download patch file">
            {copiedPatch ? <CheckIcon size={13} /> : <FileTextIcon size={13} />}
            <span>{copiedPatch ? "Downloaded" : ".patch"}</span>
          </button>

          <button className="diff-btn-action" onClick={handleCopyCode} title="Copy fixed code">
            {copied ? <CheckIcon size={13} /> : <CopyIcon size={13} />}
            <span>{copied ? "Copied" : "Copy Fix"}</span>
          </button>
        </div>
      </div>

      {/* Mode 1: Unified Diff */}
      {viewMode === "diff" && (
        <div className="diff-code-container unified">
          {diff_lines && diff_lines.length > 0 ? (
            diff_lines.map((item, idx) => {
              const isAdded = item.type === "added";
              const isRemoved = item.type === "removed";
              return (
                <div
                  key={idx}
                  className={`diff-line ${isAdded ? "line-added" : isRemoved ? "line-removed" : "line-context"}`}
                >
                  <span className="diff-line-num">{idx + 1}</span>
                  <span className="diff-line-sign">{isAdded ? "+" : isRemoved ? "-" : " "}</span>
                  <span className="diff-line-code">{item.text.replace(/^[+-]/, "")}</span>
                </div>
              );
            })
          ) : (
            <pre className="code-pre">{remediation.code_patch}</pre>
          )}
        </div>
      )}

      {/* Mode 2: Split View (Before vs After) */}
      {viewMode === "split" && (
        <div className="diff-split-container">
          <div className="split-column split-before">
            <div className="split-column-header">
              <span className="split-pill pill-before">Before (Buggy)</span>
            </div>
            <pre className="split-code before">{before_code || "// Original code"}</pre>
          </div>

          <div className="split-column split-after">
            <div className="split-column-header">
              <span className="split-pill pill-after">After (Remediated)</span>
            </div>
            <pre className="split-code after">{after_code || remediation.code_patch}</pre>
          </div>
        </div>
      )}

      {/* Mode 3: Clean Fixed Code Only */}
      {viewMode === "fixed" && (
        <div className="diff-code-container fixed">
          <pre className="code-pre">{after_code || remediation.code_patch}</pre>
        </div>
      )}
    </div>
  );
}
