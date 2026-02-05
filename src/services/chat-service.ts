'use client';

/**
 * Service for interacting with the AI Chat API
 */

interface ChatRequest {
  message: string;
  conversation_id?: string;
  metadata?: Record<string, any>;
}

interface ChatResponse {
  conversation_id: string;
  message_id: string;
  response: string;
  intent: {
    type: string;
    confidence: number;
    action_taken: string;
  };
  timestamp: string;
  next_action: string;
}

class ChatAPIService {
  private baseURL: string;

  constructor(baseURL: string = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000') {
    this.baseURL = baseURL;
  }

  /**
   * Send a message to the AI chat endpoint
   */
  async sendMessage(userId: string, request: ChatRequest): Promise<ChatResponse> {
    try {
      // Import tokenStorage to access the stored authentication token
      const tokenStorage = (await import('./api')).tokenStorage;

      const response = await fetch(`${this.baseURL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${tokenStorage.getToken() || ''}`,
        },
        body: JSON.stringify({
          message: request.message,
          conversation_id: request.conversation_id,
          metadata: request.metadata,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error sending message:', error);
      throw error;
    }
  }

  /**
   * Get a user's conversations
   */
  async getConversations(userId: string, page: number = 1, limit: number = 10): Promise<any> {
    try {
      // Import tokenStorage to access the stored authentication token
      const tokenStorage = (await import('./api')).tokenStorage;

      const response = await fetch(`${this.baseURL}/api/${userId}/conversations?page=${page}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${tokenStorage.getToken() || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching conversations:', error);
      throw error;
    }
  }

  /**
   * Get messages for a specific conversation
   */
  async getConversationMessages(userId: string, conversationId: string, page: number = 1, limit: number = 20): Promise<any> {
    try {
      // Import tokenStorage to access the stored authentication token
      const tokenStorage = (await import('./api')).tokenStorage;

      const response = await fetch(`${this.baseURL}/api/${userId}/conversations/${conversationId}/messages?page=${page}&limit=${limit}`, {
        headers: {
          'Authorization': `Bearer ${tokenStorage.getToken() || ''}`,
        },
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Error fetching conversation messages:', error);
      throw error;
    }
  }
}

export default new ChatAPIService();