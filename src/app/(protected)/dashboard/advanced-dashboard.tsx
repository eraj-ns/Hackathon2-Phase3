'use client';

import { useState, useEffect } from 'react';
import { authService } from '@/services/auth';
import { useRouter } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Plus,
  Search,
  Filter,
  Calendar,
  Bell,
  Settings,
  User,
  LogOut,
  CheckCircle2,
  Circle,
  Trash2,
  Edit3,
  MoreVertical,
  TrendingUp,
  Target,
  Clock,
  Moon,
  Sun,
  BarChart3,
  List,
  Grid3X3,
  ChevronDown,
  Archive,
  Flag,
  MessageCircle
} from 'lucide-react';
import { useTheme } from '@/contexts/ThemeContext';

interface ExtendedTask {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate?: string;
  category?: string;
  createdAt: string;
  updatedAt: string;
}

export default function AdvancedDashboard() {
  const [tasks, setTasks] = useState<ExtendedTask[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<ExtendedTask[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [filter, setFilter] = useState<'all' | 'active' | 'completed'>('all');
  const [priorityFilter, setPriorityFilter] = useState<'all' | 'low' | 'medium' | 'high'>('all');
  const [viewMode, setViewMode] = useState<'list' | 'grid'>('list');
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium' as 'low' | 'medium' | 'high',
    dueDate: '',
    category: ''
  });
  const [editingTask, setEditingTask] = useState<ExtendedTask | null>(null);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [stats, setStats] = useState({
    total: 0,
    completed: 0,
    active: 0,
    overdue: 0
  });

  const router = useRouter();
  const { theme, toggleTheme } = useTheme();

  useEffect(() => {
    if (!authService.isAuthenticated()) {
      router.push('/signin');
      return;
    }
    fetchTasks();
  }, []);

  useEffect(() => {
    filterTasks();
  }, [tasks, searchTerm, filter, priorityFilter]);

  useEffect(() => {
    calculateStats();
  }, [tasks]);

  const fetchTasks = async () => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
        headers: {
          'Authorization': `Bearer ${authService.getToken()}`
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          router.push('/signin');
          return;
        }
        throw new Error('Failed to fetch tasks');
      }

      const data = await response.json();
      // Map API response to match our ExtendedTask interface
      const mappedTasks = data.map((task: any) => ({
        id: task.id,
        title: task.title,
        description: task.description,
        completed: task.completed,
        priority: task.priority || 'medium',
        dueDate: task.due_date || task.dueDate || undefined,  // Handle both snake_case and camelCase
        category: task.category || undefined,
        createdAt: task.created_at || task.createdAt,
        updatedAt: task.updated_at || task.updatedAt
      }));
      setTasks(mappedTasks);
    } catch (err: any) {
      setError(err.message || 'Error fetching tasks');
    } finally {
      setLoading(false);
    }
  };

  const calculateStats = () => {
    const total = tasks.length;
    const completed = tasks.filter(t => t.completed).length;
    const active = total - completed;
    const overdue = tasks.filter(t =>
      !t.completed && t.dueDate && new Date(t.dueDate) < new Date()
    ).length;

    setStats({ total, completed, active, overdue });
  };

  const filterTasks = () => {
    let filtered = [...tasks];

    // Apply search filter
    if (searchTerm) {
      filtered = filtered.filter(task =>
        task.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        (task.description && task.description.toLowerCase().includes(searchTerm.toLowerCase()))
      );
    }

    // Apply status filter
    if (filter === 'active') {
      filtered = filtered.filter(task => !task.completed);
    } else if (filter === 'completed') {
      filtered = filtered.filter(task => task.completed);
    }

    // Apply priority filter
    if (priorityFilter !== 'all') {
      filtered = filtered.filter(task => task.priority === priorityFilter);
    }

    setFilteredTasks(filtered);
  };

  const handleAddTask = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authService.getToken()}`
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
          dueDate: newTask.dueDate || undefined,
          category: newTask.category || undefined
        })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          router.push('/signin');
          return;
        }
        throw new Error('Failed to add task');
      }

      const data = await response.json();
      // Map API response to match our ExtendedTask interface
      const createdTask = {
        id: data.id,
        title: data.title,
        description: data.description,
        completed: data.completed,
        priority: data.priority || 'medium',
        dueDate: data.due_date || data.dueDate || undefined,
        category: data.category || undefined,
        createdAt: data.created_at || data.createdAt,
        updatedAt: data.updated_at || data.updatedAt
      };
      setTasks([...tasks, createdTask]);
      setNewTask({
        title: '',
        description: '',
        priority: 'medium',
        dueDate: '',
        category: ''
      });
    } catch (err: any) {
      setError(err.message || 'Error adding task');
    }
  };

  const handleToggleComplete = async (taskId: string, completed: boolean) => {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authService.getToken()}`
        },
        body: JSON.stringify({ completed: !completed })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          router.push('/signin');
          return;
        }
        throw new Error('Failed to update task');
      }

      const data = await response.json();
      // Map API response to match our ExtendedTask interface
      const updatedTask = {
        id: data.id,
        title: data.title,
        description: data.description,
        completed: data.completed,
        priority: data.priority || 'medium',
        dueDate: data.due_date || data.dueDate || undefined,
        category: data.category || undefined,
        createdAt: data.created_at || data.createdAt,
        updatedAt: data.updated_at || data.updatedAt
      };
      setTasks(tasks.map(task =>
        task.id === taskId ? updatedTask : task
      ));
    } catch (err: any) {
      setError(err.message || 'Error updating task');
    }
  };

  const handleEditTask = (task: ExtendedTask) => {
    setEditingTask(task);
    setNewTask({
      title: task.title,
      description: task.description || '',
      priority: task.priority,
      dueDate: task.dueDate || '',
      category: task.category || ''
    });
  };

  const handleUpdateTask = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!editingTask) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${editingTask.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${authService.getToken()}`
        },
        body: JSON.stringify({
          title: newTask.title,
          description: newTask.description,
          priority: newTask.priority,
          dueDate: newTask.dueDate || undefined,
          category: newTask.category || undefined
        })
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          router.push('/signin');
          return;
        }
        throw new Error('Failed to update task');
      }

      const data = await response.json();
      // Map API response to match our ExtendedTask interface
      const updatedTask = {
        id: data.id,
        title: data.title,
        description: data.description,
        completed: data.completed,
        priority: data.priority || 'medium',
        dueDate: data.due_date || data.dueDate || undefined,
        category: data.category || undefined,
        createdAt: data.created_at || data.createdAt,
        updatedAt: data.updated_at || data.updatedAt
      };
      setTasks(tasks.map(task =>
        task.id === editingTask.id ? updatedTask : task
      ));
      setEditingTask(null);
      setNewTask({
        title: '',
        description: '',
        priority: 'medium',
        dueDate: '',
        category: ''
      });
    } catch (err: any) {
      setError(err.message || 'Error updating task');
    }
  };

  const handleDeleteTask = async (taskId: string) => {
    if (!window.confirm('Are you sure you want to delete this task?')) return;

    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/tasks/${taskId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${authService.getToken()}`
        }
      });

      if (!response.ok) {
        if (response.status === 401) {
          authService.logout();
          router.push('/signin');
          return;
        }
        throw new Error('Failed to delete task');
      }

      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err: any) {
      setError(err.message || 'Error deleting task');
    }
  };

  const handleCancelEdit = () => {
    setEditingTask(null);
    setNewTask({
      title: '',
      description: '',
      priority: 'medium',
      dueDate: '',
      category: ''
    });
  };

  const getPriorityColor = (priority: string) => {
    if (theme === 'dark') {
      switch (priority) {
        case 'high': return 'text-red-400 bg-red-900/30 border-red-700';
        case 'medium': return 'text-yellow-400 bg-yellow-900/30 border-yellow-700';
        case 'low': return 'text-green-400 bg-green-900/30 border-green-700';
        default: return 'text-gray-400 bg-gray-700 border-gray-600';
      }
    } else {
      switch (priority) {
        case 'high': return 'text-red-600 bg-red-50 border-red-200';
        case 'medium': return 'text-yellow-600 bg-yellow-50 border-yellow-200';
        case 'low': return 'text-green-600 bg-green-50 border-green-200';
        default: return 'text-gray-600 bg-gray-50 border-gray-200';
      }
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  const getPriorityClass = (priority: string) => {
    switch (priority) {
      case 'high': return 'task-priority-high';
      case 'medium': return 'task-priority-medium';
      case 'low': return 'task-priority-low';
      default: return '';
    }
  };

  const getPriorityBadgeClass = (priority: string) => {
    switch (priority) {
      case 'high': return 'task-priority-high-badge';
      case 'medium': return 'task-priority-medium-badge';
      case 'low': return 'task-priority-low-badge';
      default: return '';
    }
  };

  if (loading) {
    return (
      <div className={`min-h-screen bg-gradient-to-br ${theme === 'dark' ? 'from-gray-900 to-gray-800 text-white' : 'from-slate-50 to-blue-50 text-gray-900'}`}>
        <div className="flex">
          {/* Sidebar */}
          <div className={`w-64 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} shadow-lg h-screen fixed`}>
            <div className="p-6">
              <h1 className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-800'}`}>TodoPro</h1>
            </div>
            <div className="p-4">
              <div className="animate-pulse space-y-4">
                <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-3/4`}></div>
                <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-1/2`}></div>
                <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-2/3`}></div>
              </div>
            </div>
          </div>

          {/* Main Content */}
          <div className={`ml-64 flex-1 p-8 ${theme === 'dark' ? 'bg-gray-900' : 'bg-transparent'}`}>
            <div className="max-w-6xl mx-auto">
              <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                {[1, 2, 3, 4].map((item) => (
                  <div key={item} className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} p-6 rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'}`}>
                    <div className="animate-pulse">
                      <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-1/2 mb-2`}></div>
                      <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-8 rounded w-1/4`}></div>
                    </div>
                  </div>
                ))}
              </div>

              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} p-6`}>
                <div className="animate-pulse space-y-4">
                  <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-full`}></div>
                  <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-3/4`}></div>
                  <div className={`${theme === 'dark' ? 'bg-gray-600' : 'bg-gray-200'} h-4 rounded w-1/2`}></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className={`min-h-screen bg-gradient-to-br ${theme === 'dark' ? 'from-gray-900 to-gray-800 text-white' : 'from-slate-50 to-blue-50 text-gray-900'}`}>
      <div className="flex">
        {/* Sidebar */}
        <motion.div
          initial={{ x: -300 }}
          animate={{ x: 0 }}
          className={`w-64 ${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} shadow-lg h-screen fixed z-10`}
        >
          <div className={`p-6 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'}`}>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              TodoPro
            </h1>
            <p className={`text-sm ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} mt-1`}>Advanced Task Management</p>
          </div>

          <div className="p-4 space-y-2">
            <button
              onClick={() => setFilter('all')}
              className={`w-full text-left p-3 rounded-lg transition-all ${
                filter === 'all'
                  ? `${theme === 'dark' ? 'bg-blue-900/30 text-blue-300 border-l-4 border-blue-500' : 'bg-blue-50 text-blue-700 border-l-4 border-blue-600'}`
                  : `${theme === 'dark' ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-50 text-gray-700'}`
              }`}
            >
              <div className="flex items-center gap-3">
                <Target className="w-5 h-5" />
                <span>All Tasks</span>
                <span className={`ml-auto ${theme === 'dark' ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'} text-xs px-2 py-1 rounded-full`}>
                  {stats.total}
                </span>
              </div>
            </button>

            <button
              onClick={() => setFilter('active')}
              className={`w-full text-left p-3 rounded-lg transition-all ${
                filter === 'active'
                  ? `${theme === 'dark' ? 'bg-orange-900/30 text-orange-300 border-l-4 border-orange-500' : 'bg-orange-50 text-orange-700 border-l-4 border-orange-600'}`
                  : `${theme === 'dark' ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-50 text-gray-700'}`
              }`}
            >
              <div className="flex items-center gap-3">
                <Clock className="w-5 h-5" />
                <span>Active</span>
                <span className={`ml-auto ${theme === 'dark' ? 'bg-orange-900/30 text-orange-300' : 'bg-orange-100 text-orange-600'} text-xs px-2 py-1 rounded-full`}>
                  {stats.active}
                </span>
              </div>
            </button>

            <button
              onClick={() => setFilter('completed')}
              className={`w-full text-left p-3 rounded-lg transition-all ${
                filter === 'completed'
                  ? `${theme === 'dark' ? 'bg-green-900/30 text-green-300 border-l-4 border-green-500' : 'bg-green-50 text-green-700 border-l-4 border-green-600'}`
                  : `${theme === 'dark' ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-50 text-gray-700'}`
              }`}
            >
              <div className="flex items-center gap-3">
                <CheckCircle2 className="w-5 h-5" />
                <span>Completed</span>
                <span className={`ml-auto ${theme === 'dark' ? 'bg-green-900/30 text-green-300' : 'bg-green-100 text-green-600'} text-xs px-2 py-1 rounded-full`}>
                  {stats.completed}
                </span>
              </div>
            </button>

            <div className="pt-4 border-t border-gray-700">
              <button
                onClick={() => router.push('/chat')}
                className={`w-full text-left p-3 rounded-lg transition-all ${theme === 'dark' ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-50 text-gray-700'}`}
              >
                <div className="flex items-center gap-3">
                  <BarChart3 className="w-5 h-5" />
                  <span>Analytics</span>
                </div>
              </button>


              <button className={`w-full text-left p-3 rounded-lg transition-all ${theme === 'dark' ? 'hover:bg-gray-700 text-gray-300' : 'hover:bg-gray-50 text-gray-700'}`}>
                <div className="flex items-center gap-3">
                  <Archive className="w-5 h-5" />
                  <span>Archived</span>
                </div>
              </button>
            </div>
          </div>

          <div className={`p-4 border-t ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} mt-auto`}>
            <div
              onClick={toggleTheme}
              className={`flex items-center gap-3 p-3 rounded-lg ${theme === 'dark' ? 'hover:bg-gray-700 cursor-pointer' : 'hover:bg-gray-50 cursor-pointer'}`}
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5 text-gray-300" />
              ) : (
                <Moon className="w-5 h-5 text-gray-600" />
              )}
              <span className={`${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Switch to {theme === 'dark' ? 'Light' : 'Dark'} Mode</span>
            </div>
            <div className={`flex items-center gap-3 p-3 rounded-lg ${theme === 'dark' ? 'hover:bg-gray-700 cursor-pointer' : 'hover:bg-gray-50 cursor-pointer'}`}>
              <User className={`w-5 h-5 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Profile</span>
            </div>
            <div className={`flex items-center gap-3 p-3 rounded-lg ${theme === 'dark' ? 'hover:bg-gray-700 cursor-pointer' : 'hover:bg-gray-50 cursor-pointer'}`}>
              <Settings className={`w-5 h-5 ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`} />
              <span className={`${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'}`}>Settings</span>
            </div>
            <div
              onClick={() => {
                authService.logout();
                router.push('/signin');
              }}
              className={`flex items-center gap-3 p-3 rounded-lg ${theme === 'dark' ? 'hover:bg-red-900/30 cursor-pointer text-red-400' : 'hover:bg-red-50 cursor-pointer text-red-600'}`}
            >
              <LogOut className="w-5 h-5" />
              <span>Logout</span>
            </div>
          </div>
        </motion.div>

        {/* Main Content */}
        <div className="ml-64 flex-1 p-8">
          <div className="max-w-6xl mx-auto">
            {/* AI Chat Button - Positioned prominently above stats */}
            <div className="flex justify-center mb-8">
              <button
                onClick={() => router.push('/chat')}
                className={`p-6 rounded-full shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 ${
                  theme === 'dark'
                    ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    : 'bg-gradient-to-r from-blue-500 to-purple-500 text-white'
                }`}
              >
                <div className="flex items-center gap-2">
                  <MessageCircle className="w-16 h-16" />
                  <span className="font-semibold">AI Task Assistant</span>
                </div>
              </button>
            </div>

            {/* Stats Overview */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            >
              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} p-6 rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} hover:shadow-md transition-shadow`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Total Tasks</p>
                    <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>{stats.total}</p>
                  </div>
                  <div className={`${theme === 'dark' ? 'bg-blue-900/30' : 'bg-blue-50'} p-3 rounded-full`}>
                    <Target className={`w-6 h-6 ${theme === 'dark' ? 'text-blue-400' : 'text-blue-600'}`} />
                  </div>
                </div>
              </div>

              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} p-6 rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} hover:shadow-md transition-shadow`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Completed</p>
                    <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`}>{stats.completed}</p>
                  </div>
                  <div className={`${theme === 'dark' ? 'bg-green-900/30' : 'bg-green-50'} p-3 rounded-full`}>
                    <CheckCircle2 className={`w-6 h-6 ${theme === 'dark' ? 'text-green-400' : 'text-green-600'}`} />
                  </div>
                </div>
              </div>

              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} p-6 rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} hover:shadow-md transition-shadow`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Active</p>
                    <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-orange-400' : 'text-orange-600'}`}>{stats.active}</p>
                  </div>
                  <div className={`${theme === 'dark' ? 'bg-orange-900/30' : 'bg-orange-50'} p-3 rounded-full`}>
                    <Clock className={`w-6 h-6 ${theme === 'dark' ? 'text-orange-400' : 'text-orange-600'}`} />
                  </div>
                </div>
              </div>

              <div className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} p-6 rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} hover:shadow-md transition-shadow`}>
                <div className="flex items-center justify-between">
                  <div>
                    <p className={`text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-600'}`}>Overdue</p>
                    <p className={`text-2xl font-bold ${theme === 'dark' ? 'text-red-400' : 'text-red-600'}`}>{stats.overdue}</p>
                  </div>
                  <div className={`${theme === 'dark' ? 'bg-red-900/30' : 'bg-red-50'} p-3 rounded-full`}>
                    <Bell className={`w-6 h-6 ${theme === 'dark' ? 'text-red-400' : 'text-red-600'}`} />
                  </div>
                </div>
              </div>
            </motion.div>

            {/* Controls */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} p-6 mb-8`}
            >
              <div className="flex flex-col lg:flex-row gap-4 items-center justify-between">
                <div className="flex flex-col sm:flex-row gap-4 flex-1">
                  <div className="relative flex-1 max-w-md">
                    <Search className={`absolute left-3 top-1/2 transform -translate-y-1/2 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-400'} w-5 h-5`} />
                    <input
                      type="text"
                      placeholder="Search tasks..."
                      value={searchTerm}
                      onChange={(e) => setSearchTerm(e.target.value)}
                      className={`w-full pl-10 pr-4 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    />
                  </div>

                  <select
                    value={priorityFilter}
                    onChange={(e) => setPriorityFilter(e.target.value as any)}
                    className={`px-4 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                  >
                    <option value="all" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>All Priorities</option>
                    <option value="high" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>High Priority</option>
                    <option value="medium" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>Medium Priority</option>
                    <option value="low" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>Low Priority</option>
                  </select>

                  <div className="flex gap-2">
                    <button
                      onClick={() => setViewMode('list')}
                      className={`p-2 border ${viewMode === 'list' ? 'border-blue-500 bg-blue-50' : theme === 'dark' ? 'border-gray-600 hover:bg-gray-700' : 'border-gray-200 hover:bg-gray-50'} rounded-lg`}
                    >
                      <List className="w-5 h-5" />
                    </button>
                    <button
                      onClick={() => setViewMode('grid')}
                      className={`p-2 border ${viewMode === 'grid' ? 'border-blue-500 bg-blue-50' : theme === 'dark' ? 'border-gray-600 hover:bg-gray-700' : 'border-gray-200 hover:bg-gray-50'} rounded-lg`}
                    >
                      <Grid3X3 className="w-5 h-5" />
                    </button>
                  </div>
                </div>

                <button
                  onClick={() => setSidebarOpen(!sidebarOpen)}
                  className={`lg:hidden p-2 border ${theme === 'dark' ? 'border-gray-600 hover:bg-gray-700' : 'border-gray-200 hover:bg-gray-50'} rounded-lg`}
                >
                  <Filter className="w-5 h-5" />
                </button>
              </div>
            </motion.div>

            {/* Task Form */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} p-6 mb-8`}
            >
              <h2 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'} mb-4 flex items-center gap-2`}>
                {editingTask ? <Edit3 className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
                {editingTask ? 'Edit Task' : 'Create New Task'}
              </h2>

              {error && (
                <div className={`mb-4 p-3 ${theme === 'dark' ? 'bg-red-900/30 border border-red-800 text-red-200' : 'bg-red-50 border border-red-200 text-red-700'} rounded-lg`}>
                  {error}
                </div>
              )}

              <form onSubmit={editingTask ? handleUpdateTask : handleAddTask} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>
                      Task Title *
                    </label>
                    <input
                      type="text"
                      value={newTask.title}
                      onChange={(e) => setNewTask({...newTask, title: e.target.value})}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                      placeholder="What needs to be done?"
                      required
                    />
                  </div>

                  <div>
                    <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>
                      Priority
                    </label>
                    <select
                      value={newTask.priority}
                      onChange={(e) => setNewTask({...newTask, priority: e.target.value as any})}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    >
                      <option value="low" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>Low</option>
                      <option value="medium" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>Medium</option>
                      <option value="high" className={theme === 'dark' ? 'bg-gray-700 text-white' : ''}>High</option>
                    </select>
                  </div>
                </div>

                <div>
                  <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>
                    Description
                  </label>
                  <textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({...newTask, description: e.target.value})}
                    className={`w-full px-3 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    placeholder="Add details..."
                    rows={2}
                  />
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>
                      Due Date
                    </label>
                    <input
                      type="date"
                      value={newTask.dueDate}
                      onChange={(e) => setNewTask({...newTask, dueDate: e.target.value})}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                    />
                  </div>

                  <div>
                    <label className={`block text-sm font-medium ${theme === 'dark' ? 'text-gray-300' : 'text-gray-700'} mb-1`}>
                      Category
                    </label>
                    <input
                      type="text"
                      value={newTask.category}
                      onChange={(e) => setNewTask({...newTask, category: e.target.value})}
                      className={`w-full px-3 py-2 border ${theme === 'dark' ? 'border-gray-600 bg-gray-700 text-white' : 'border-gray-200'} rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent`}
                      placeholder="Work, Personal, etc."
                    />
                  </div>
                </div>

                <div className="flex gap-3 pt-2">
                  {editingTask && (
                    <button
                      type="button"
                      onClick={handleCancelEdit}
                      className={`px-4 py-2 ${theme === 'dark' ? 'text-gray-300 bg-gray-700 hover:bg-gray-600' : 'text-gray-700 bg-gray-100 hover:bg-gray-200'} rounded-lg transition-colors`}
                    >
                      Cancel
                    </button>
                  )}
                  <button
                    type="submit"
                    className="px-6 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg hover:from-blue-700 hover:to-purple-700 transition-all shadow-md hover:shadow-lg"
                  >
                    {editingTask ? 'Update Task' : 'Add Task'}
                  </button>
                </div>
              </form>
            </motion.div>

            {/* Task List */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className={`${theme === 'dark' ? 'bg-gray-800' : 'bg-white'} rounded-xl shadow-sm border ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} overflow-hidden`}
            >
              <div className={`p-6 border-b ${theme === 'dark' ? 'border-gray-700' : 'border-gray-100'} flex justify-between items-center`}>
                <h2 className={`text-lg font-semibold ${theme === 'dark' ? 'text-white' : 'text-gray-900'}`}>
                  Your Tasks ({filteredTasks.length})
                </h2>
                <div className="flex gap-2">
                  <span className={`px-3 py-1 rounded-full text-sm ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'}`}>
                    {viewMode === 'list' ? 'List View' : 'Grid View'}
                  </span>
                </div>
              </div>

              <div className={theme === 'dark' ? 'divide-y divide-gray-700' : 'divide-y divide-gray-100'}>
                <AnimatePresence>
                  {filteredTasks.length === 0 ? (
                    <motion.div
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      className="p-12 text-center"
                    >
                      <div className={`w-16 h-16 ${theme === 'dark' ? 'bg-gray-700' : 'bg-gray-100'} rounded-full flex items-center justify-center mx-auto mb-4`}>
                        <Target className={`w-8 h-8 ${theme === 'dark' ? 'text-gray-400' : 'text-gray-400'}`} />
                      </div>
                      <h3 className={`text-lg font-medium ${theme === 'dark' ? 'text-white' : 'text-gray-900'} mb-2`}>No tasks found</h3>
                      <p className={`${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'}`}>Create your first task to get started!</p>
                    </motion.div>
                  ) : viewMode === 'list' ? (
                    filteredTasks.map((task) => (
                      <motion.div
                        key={task.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        exit={{ opacity: 0, x: 20 }}
                        className={`p-6 ${theme === 'dark' ? 'hover:bg-gray-700/50' : 'hover:bg-gray-50'} transition-colors ${
                          task.completed ? (theme === 'dark' ? 'bg-green-900/20' : 'bg-green-50/30') : ''
                        } ${getPriorityClass(task.priority)}`}
                      >
                        <div className="flex items-start gap-4">
                          <button
                            onClick={() => handleToggleComplete(task.id, task.completed)}
                            className={`mt-1 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-all ${
                              task.completed
                                ? `${theme === 'dark' ? 'bg-green-500 border-green-500' : 'bg-green-500 border-green-500'} text-white`
                                : `${theme === 'dark' ? 'border-gray-500 hover:border-green-400' : 'border-gray-300 hover:border-green-500'}`
                            }`}
                          >
                            {task.completed && <CheckCircle2 className="w-3 h-3" />}
                          </button>

                          <div className="flex-1 min-w-0">
                            <div className="flex items-center gap-3 mb-2">
                              <h3 className={`font-medium ${
                                task.completed
                                  ? `${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} line-through`
                                  : `${theme === 'dark' ? 'text-gray-100' : 'text-gray-900'}`
                              }`}>
                                {task.title}
                              </h3>

                              <span className={`text-xs px-2 py-1 rounded-full capitalize ${getPriorityBadgeClass(task.priority)}`}>
                                {task.priority}
                              </span>

                              {task.dueDate && (
                                <span className={`text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} flex items-center gap-1`}>
                                  <Calendar className="w-3 h-3" />
                                  {formatDate(task.dueDate)}
                                </span>
                              )}
                            </div>

                            {task.description && (
                              <p className={`text-sm mb-2 ${
                                task.completed ? (theme === 'dark' ? 'text-gray-500' : 'text-gray-400') : (theme === 'dark' ? 'text-gray-300' : 'text-gray-600')
                              }`}>
                                {task.description}
                              </p>
                            )}

                            <div className="flex flex-wrap gap-2 mt-2">
                              {task.category && (
                                <span className={`inline-block px-2 py-1 text-xs ${theme === 'dark' ? 'bg-gray-700 text-gray-300' : 'bg-gray-100 text-gray-600'} rounded-full`}>
                                  {task.category}
                                </span>
                              )}
                              {task.dueDate && new Date(task.dueDate) < new Date() && !task.completed && (
                                <span className={`inline-block px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full`}>
                                  Overdue
                                </span>
                              )}
                            </div>
                          </div>

                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleEditTask(task)}
                              className={`p-2 ${theme === 'dark' ? 'text-gray-400 hover:text-blue-400 hover:bg-blue-900/30' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'} rounded-lg transition-colors`}
                            >
                              <Edit3 className="w-4 h-4" />
                            </button>
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className={`p-2 ${theme === 'dark' ? 'text-gray-400 hover:text-red-400 hover:bg-red-900/30' : 'text-gray-400 hover:text-red-600 hover:bg-red-50'} rounded-lg transition-colors`}
                            >
                              <Trash2 className="w-4 h-4" />
                            </button>
                          </div>
                        </div>
                      </motion.div>
                    ))
                  ) : (
                    // Grid view - render tasks in a grid layout
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-4">
                      {filteredTasks.map((task) => (
                        <motion.div
                          key={task.id}
                          initial={{ opacity: 0, scale: 0.9 }}
                          animate={{ opacity: 1, scale: 1 }}
                          exit={{ opacity: 0, scale: 0.9 }}
                          className={`p-4 rounded-lg border ${theme === 'dark' ? 'border-gray-700 bg-gray-700/50' : 'border-gray-200 bg-white'} ${getPriorityClass(task.priority)} shadow-sm hover:shadow-md transition-shadow`}
                        >
                          <div className="flex items-start gap-3">
                            <button
                              onClick={() => handleToggleComplete(task.id, task.completed)}
                              className={`mt-0.5 flex-shrink-0 w-4 h-4 rounded border-2 flex items-center justify-center transition-all ${
                                task.completed
                                  ? `${theme === 'dark' ? 'bg-green-500 border-green-500' : 'bg-green-500 border-green-500'} text-white`
                                  : `${theme === 'dark' ? 'border-gray-500 hover:border-green-400' : 'border-gray-300 hover:border-green-500'}`
                              }`}
                            >
                              {task.completed && <CheckCircle2 className="w-2 h-2" />}
                            </button>

                            <div className="flex-1">
                              <h4 className={`font-medium text-sm mb-1 ${
                                task.completed
                                  ? `${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} line-through`
                                  : `${theme === 'dark' ? 'text-gray-100' : 'text-gray-900'}`
                              }`}>
                                {task.title}
                              </h4>

                              {task.description && (
                                <p className={`text-xs mb-2 ${
                                  task.completed ? (theme === 'dark' ? 'text-gray-500' : 'text-gray-400') : (theme === 'dark' ? 'text-gray-300' : 'text-gray-600')
                                }`}>
                                  {task.description?.substring(0, 60)}...
                                </p>
                              )}

                              <div className="flex flex-wrap gap-1 mt-2">
                                <span className={`text-xs px-1.5 py-0.5 rounded-full capitalize ${getPriorityBadgeClass(task.priority)}`}>
                                  {task.priority}
                                </span>

                                {task.category && (
                                  <span className={`inline-block px-1.5 py-0.5 text-xs ${theme === 'dark' ? 'bg-gray-600 text-gray-300' : 'bg-gray-100 text-gray-600'} rounded-full`}>
                                    {task.category}
                                  </span>
                                )}

                                {task.dueDate && (
                                  <span className={`text-xs ${theme === 'dark' ? 'text-gray-400' : 'text-gray-500'} flex items-center gap-0.5`}>
                                    <Calendar className="w-2 h-2" />
                                    {formatDate(task.dueDate)}
                                  </span>
                                )}
                              </div>
                            </div>
                          </div>

                          <div className="flex justify-end gap-1 mt-3">
                            <button
                              onClick={() => handleEditTask(task)}
                              className={`p-1.5 ${theme === 'dark' ? 'text-gray-400 hover:text-blue-400 hover:bg-blue-900/30' : 'text-gray-400 hover:text-blue-600 hover:bg-blue-50'} rounded transition-colors`}
                            >
                              <Edit3 className="w-3 h-3" />
                            </button>
                            <button
                              onClick={() => handleDeleteTask(task.id)}
                              className={`p-1.5 ${theme === 'dark' ? 'text-gray-400 hover:text-red-400 hover:bg-red-900/30' : 'text-gray-400 hover:text-red-600 hover:bg-red-50'} rounded transition-colors`}
                            >
                              <Trash2 className="w-3 h-3" />
                            </button>
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  )}
                </AnimatePresence>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}