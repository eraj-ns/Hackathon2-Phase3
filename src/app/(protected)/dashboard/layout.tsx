/**
 * Modern Dashboard Layout Component
 * Updated with contemporary UI design
 */

import { ReactNode } from "react";

export default function DashboardLayout({ children }: { children: ReactNode }) {
  return (
    <main className="dashboard-content">
      {children}
    </main>
  );
}