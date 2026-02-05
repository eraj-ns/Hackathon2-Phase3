'use client';

import { useState, useRef, useEffect } from 'react';
import { authService } from '@/services/auth';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function ChatPage() {
  const [userId, setUserId] = useState<string | null>(null);

  // Check if user is authenticated and get user ID
  useEffect(() => {
    if (authService.isAuthenticated()) {
      // In a real implementation, you would get the user ID from the token or API
      // For now, we'll just check authentication status
      setUserId('current_user'); // Placeholder - would be replaced with actual user ID
    }
  }, []);
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<null | HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading || !authService.isAuthenticated()) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Get user ID from the auth service
      // In a real implementation, you would decode the JWT token to get the user ID
      // For now, we'll use the token to make the API call
      if (!authService.getToken()) {
        throw new Error('User not authenticated');
      }

      // Decode the JWT token to get user ID (simplified approach)
      const token = authService.getToken();
      let userId = 'unknown';

      if (token) {
        try {
          // Decode JWT token to extract user ID
          const base64Url = token.split('.')[1];
          const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
          const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
            return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
          }).join(''));

          const decodedToken = JSON.parse(jsonPayload);
          userId = decodedToken.sub; // 'sub' is the standard claim for subject/user ID in JWT
        } catch (decodeError) {
          console.error('Error decoding token:', decodeError);
          // If we can't decode the token, we might need to make an API call to get user info
          // For now, we'll proceed with a placeholder
        }
      }

      // Use the chat service to call the backend API
      const chatService = (await import('@/services/chat-service')).default;
      const data = await chatService.sendMessage(userId, {
        message: input,
      });

      // Add AI response
      const aiMessage: Message = {
        id: data.message_id,
        role: 'assistant',
        content: data.response,
        timestamp: data.timestamp,
      };

      setMessages(prev => [...prev, aiMessage]);
    } catch (error: any) {
      console.error('Error in chat:', error);

      // Set error state
      setError(error.message || 'Sorry, I encountered an error processing your request. Please try again.');

      // Add error message
      const errorMessage: Message = {
        id: Date.now().toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error processing your request. Please try again.',
        timestamp: new Date().toISOString(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
      // Clear error after a delay
      setTimeout(() => {
        setError(null);
      }, 5000);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm py-4 px-6">
        <h1 className="text-xl font-semibold text-gray-800">AI Task Assistant</h1>
      </header>

      {/* Error Display */}
      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
          <span className="block sm:inline">{error}</span>
        </div>
      )}

      {/* Chat Container */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 ? (
          <div className="text-center text-gray-500 mt-20">
            <p>Start a conversation with the AI assistant to manage your tasks!</p>
            <p className="mt-2">Try saying: "Add a task to buy groceries tomorrow"</p>
          </div>
        ) : (
          messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${
                message.role === 'user' ? 'justify-end' : 'justify-start'
              }`}
            >
              <div
                className={`max-w-[80%] rounded-lg px-4 py-2 ${
                  message.role === 'user'
                    ? 'bg-blue-500 text-white'
                    : 'bg-gray-200 text-gray-800'
                }`}
              >
                <div className="whitespace-pre-wrap">{message.content}</div>
                <div className="text-xs opacity-70 mt-1">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </div>
              </div>
            </div>
          ))
        )}
        {isLoading && (
          <div className="flex justify-start">
            <div className="bg-gray-200 text-gray-800 rounded-lg px-4 py-2 max-w-[80%]">
              <div>Thinking...</div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Form */}
      <div className="bg-white border-t p-4">
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type your message here..."
            disabled={isLoading}
            className="flex-1 border border-gray-300 rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-blue-500 text-white rounded-lg px-6 py-2 hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </form>
        <p className="text-xs text-gray-500 mt-2">
          Tip: You can ask me to create, view, update, or manage your tasks
        </p>
      </div>
    </div>
  );
}