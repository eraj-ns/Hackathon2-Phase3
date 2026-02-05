/**
 * Root Page with Redirect Logic
 * Spec-3: Frontend Application & Full-Stack Integration
 * Redirects authenticated users to dashboard, unauthenticated to signin
 */

"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { authService } from "@/services/auth";
import { LoadingSpinner } from "@/components/LoadingSpinner";

export default function HomePage() {
  const router = useRouter();

  useEffect(() => {
    // Check if user is authenticated
    if (authService.isAuthenticated()) {
      // Redirect to dashboard
      router.push("/dashboard");
    } else {
      // Redirect to signin
      router.push("/signin");
    }
  }, [router]);

  return (
    <div className="spinner-container">
      <LoadingSpinner message="Checking authentication..." />
    </div>
  );
}
