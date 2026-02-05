/**
 * LoadingSpinner Component
 * Spec-3: Frontend Application & Full-Stack Integration
 * Displays loading indicator with optional message
 */

"use client";

import React from "react";
import { LoadingSpinnerProps } from "@/types";

export function LoadingSpinner({
  message,
  size = "medium",
}: LoadingSpinnerProps): React.ReactNode {
  const sizeClass =
    size === "large"
      ? "spinner-large"
      : size === "small"
        ? ""
        : "";

  return (
    <div className="spinner-container">
      <div style={{ textAlign: "center" }}>
        <div className={`spinner ${sizeClass}`}></div>
        {message && (
          <p style={{ marginTop: "1rem", color: "#666" }}>
            {message}
          </p>
        )}
      </div>
    </div>
  );
}
