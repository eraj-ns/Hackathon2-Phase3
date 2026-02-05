/**
 * ErrorBanner Component
 * Spec-3: Frontend Application & Full-Stack Integration
 * Displays error messages with dismiss and retry options
 */

"use client";

import React from "react";
import { APIError, ErrorBannerProps } from "@/types";

export function ErrorBanner({
  error,
  onDismiss,
  onRetry,
}: ErrorBannerProps): React.ReactNode {
  if (!error) return null;

  const message =
    typeof error === "string"
      ? error
      : (error as APIError).message || "An error occurred";

  const isValidationError =
    typeof error !== "string" && (error as APIError).status === 422;

  return (
    <div className="error-banner" role="alert">
      <div style={{ marginBottom: "0.5rem" }}>
        <strong>Error:</strong> {message}
      </div>

      {isValidationError && typeof error !== "string" && (
        <div style={{ marginBottom: "0.75rem", fontSize: "0.875rem" }}>
          {Object.entries((error as APIError).details || {}).map(
            ([field, detail]) => (
              <div key={field} style={{ marginLeft: "1rem" }}>
                • <strong>{field}:</strong> {String(detail)}
              </div>
            )
          )}
        </div>
      )}

      <div style={{ display: "flex", gap: "0.5rem" }}>
        {onRetry && (
          <button
            onClick={onRetry}
            style={{
              backgroundColor: "#c62828",
              padding: "0.5rem 1rem",
              fontSize: "0.875rem",
            }}
          >
            Retry
          </button>
        )}

        {onDismiss && (
          <button
            onClick={onDismiss}
            className="secondary"
            style={{
              padding: "0.5rem 1rem",
              fontSize: "0.875rem",
            }}
          >
            Dismiss
          </button>
        )}
      </div>
    </div>
  );
}
