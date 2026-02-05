/**
 * Modern Auth Layout Component
 * Updated with contemporary UI design
 */

import { ReactNode } from "react";

export default function AuthLayout({ children }: { children: ReactNode }) {
  return (
    <div className="auth-form-container">
      <div className="auth-card">
        <div className="auth-header">
          <h1>Todo App</h1>
          <p className="auth-subtitle">Manage your tasks efficiently</p>
        </div>
        {children}
      </div>
    </div>
  );
}