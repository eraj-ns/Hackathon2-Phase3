/**
 * Modern Navbar Component
 * Updated with contemporary UI design
 */

"use client";

import React from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth";

export function Navbar(): React.ReactNode {
  const router = useRouter();

  const handleLogout = () => {
    authService.logout();
    router.push("/signin");
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">📋 Todo App</div>

      <div className="navbar-content">
        <button
          onClick={handleLogout}
          className="btn btn-outline"
        >
          Logout
        </button>
      </div>
    </nav>
  );
}
