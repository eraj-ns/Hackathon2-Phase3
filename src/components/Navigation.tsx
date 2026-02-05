// src/components/Navigation.tsx
'use client';

import Link from 'next/link';
import { useAuth } from '@/contexts/AuthContext';
import ThemeToggle from './ThemeToggle';

export default function Navigation() {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
    // The page will automatically redirect due to the protected layout
  };

  return (
    <nav className="navbar">
      <div className="navbar-brand">
        <Link href="/">📋 Todo App</Link>
      </div>
      <div className="navbar-content">
        <ThemeToggle />
        {user ? (
          <div className="flex items-center space-x-4">
            <span className="text-sm">{user.email}</span>
            <button
              onClick={handleLogout}
              className="btn btn-outline"
            >
              Logout
            </button>
          </div>
        ) : (
          <div className="flex space-x-4">
            <Link href="/signin" className="btn btn-outline">
              Sign In
            </Link>
            <Link href="/signup" className="btn btn-primary">
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}