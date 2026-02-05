/**
 * Frontend Data Models & Type Definitions
 * Spec-3: Frontend Application & Full-Stack Integration
 */

// User Entity (from Spec-2, consumed by frontend)
export interface User {
  id: string;
  email: string;
  name?: string;
  createdAt: string;
  lastLogin?: string;
}

// Task Entity (from Spec-1, consumed by frontend)
export interface Task {
  id: string;
  userId: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  category?: string;
  createdAt: string;
  updatedAt: string;
}

// Authentication State
export interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error?: string;
}

// Session Entity (from Spec-2, managed by frontend)
export interface Session {
  token: string;
  user: User;
  expiresAt: string;
  isValid: boolean;
}

// API Error Response
export interface APIError {
  status: number;
  code: string;
  message: string;
  details?: Record<string, unknown>;
}

// Task Management State
export interface TasksState {
  items: Task[];
  loading: boolean;
  error?: string;
  lastSyncAt?: string;
}

// App Context Type
export interface AppContextType {
  auth: AuthState;
  tasks: TasksState;
  ui: {
    showNotification?: {
      type: "success" | "error" | "info";
      message: string;
    };
  };
}

// Component Props
export interface ProtectedPageProps {
  user: User;
}

export interface TaskItemProps {
  task: Task;
  onComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onUpdate: (taskId: string, title: string) => Promise<void>;
}

export interface TaskFormProps {
  onSubmit: (title: string) => Promise<void>;
  isLoading?: boolean;
  error?: string;
}

export interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  error?: string;
  onToggleComplete: (taskId: string) => Promise<void>;
  onDelete: (taskId: string) => Promise<void>;
  onUpdate: (taskId: string, title: string) => Promise<void>;
}

export interface NavbarProps {
  user?: User;
  onLogout: () => void;
}

export interface ErrorBannerProps {
  error?: APIError | string | null;
  onDismiss?: () => void;
  onRetry?: () => void;
}

export interface LoadingSpinnerProps {
  message?: string;
  size?: "small" | "medium" | "large";
}
