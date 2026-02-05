'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { authService } from '@/services/auth';
import AdvancedDashboardComponent from '../(protected)/dashboard/advanced-dashboard';

export default function TasksPage() {
  const router = useRouter();
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is authenticated before showing tasks
    if (!authService.isAuthenticated()) {
      router.push('/signin');
    } else {
      setLoading(false);
    }
  }, []);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-t-2 border-b-2 border-blue-500 mb-4"></div>
          <p className="text-gray-600">Loading task dashboard...</p>
        </div>
      </div>
    );
  }

  return <AdvancedDashboardComponent />;
}