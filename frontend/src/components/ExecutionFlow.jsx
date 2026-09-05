import React from "react";
import { CpuIcon, AlertTriangleIcon, ActivityIcon } from "./Icons";

export default function ExecutionFlow({ rootCause }) {
  if (!rootCause) return null;

  const { possible_root_cause, technical_mechanism, affected_layer, confidence, blast_radius, timeline } = rootCause;

  return (
    <div className="execution-flow-card">
      {/* Top Meta Summary */}
      <div className="flow-meta-row">
        <div className="flow-primary-cause">
          <div className="cause-icon-bubble">
            <CpuIcon size={18} />
          </div>
          <div>
            <h3 className="cause-title">{possible_root_cause}</h3>
            <p className="cause-subtitle">{technical_mechanism}</p>
          </div>
        </div>

        <div className="flow-badges-cluster">
          <div className="flow-metric-pill">
            <span className="flow-pill-label">Confidence</span>
            <span className="flow-pill-val">{confidence || "90%"}</span>
          </div>
          <div className="flow-metric-pill">
            <span className="flow-pill-label">Layer</span>
            <span className="flow-pill-val">{affected_layer || "Application"}</span>
          </div>
        </div>
      </div>

      {/* Blast Radius Section */}
      {blast_radius && blast_radius.length > 0 && (
        <div className="blast-radius-wrap">
          <span className="blast-label">
            <AlertTriangleIcon size={13} />
            Impacted Modules (Blast Radius):
          </span>
          <div className="blast-tags">
            {blast_radius.map((module, i) => (
              <span key={i} className="blast-tag">
                {module}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Execution Timeline / Causal Chain */}
      {timeline && timeline.length > 0 && (
        <div className="timeline-container">
          <h4 className="timeline-heading">
            <ActivityIcon size={14} />
            Causal Execution Cascade
          </h4>
          <div className="timeline-steps-track">
            {timeline.map((step, idx) => (
              <div key={idx} className="timeline-node">
                <div className="timeline-marker">
                  <span className="marker-dot">{step.step || idx + 1}</span>
                  {idx < timeline.length - 1 && <div className="marker-line" />}
                </div>
                <div className="timeline-body">
                  <div className="timeline-phase">{step.phase}</div>
                  <div className="timeline-detail">{step.detail}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
