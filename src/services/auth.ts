/**
 * Better Auth Client Setup
 * Spec-3: Frontend Application & Full-Stack Integration
 * Handles authentication with JWT plugin
 */

import { tokenStorage } from "./api";

/**
 * Authentication Service
 * Manages signup, signin, and logout operations
 */
export const authService = {
  /**
   * Sign up a new user
   * Calls Better Auth signup endpoint and stores JWT token
   */
  async signup(
    email: string,
    password: string,
    name?: string
  ): Promise<{ user: any; token: string }> {
    try {
      // Validate API URL
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        throw {
          status: 0,
          code: "CONFIG_ERROR",
          message: "API URL is not configured. Please check your environment variables.",
          details: {},
        };
      }

      const response = await fetch(
        `${apiUrl}/auth/signup`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, name }),
        }
      );

      if (!response.ok) {
        let errorMessage = "Signup failed";
        try {
          const error = await response.json();
          errorMessage = error.detail || error.message || errorMessage;
        } catch (e) {
          // If response is not JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }

        throw {
          status: response.status,
          code: "SIGNUP_ERROR",
          message: errorMessage,
          details: {},
        };
      }

      const data = await response.json();
      if (data.access_token) {
        tokenStorage.saveToken(data.access_token);
      }
      return { user: null, token: data.access_token };
    } catch (error: any) {
      // Handle network errors specifically
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw {
          status: 0,
          code: "NETWORK_ERROR",
          message: "Network error: Unable to reach the server. Please make sure the backend is running.",
          details: {},
        };
      }
      throw error;
    }
  },

  /**
   * Sign in an existing user
   * Calls Better Auth signin endpoint and stores JWT token
   */
  async signin(
    email: string,
    password: string
  ): Promise<{ user: any; token: string }> {
    try {
      // Validate API URL
      const apiUrl = process.env.NEXT_PUBLIC_API_URL;
      if (!apiUrl) {
        throw {
          status: 0,
          code: "CONFIG_ERROR",
          message: "API URL is not configured. Please check your environment variables.",
          details: {},
        };
      }

      // Create form data for OAuth2PasswordRequestForm - use URLSearchParams instead of FormData
      // because fetch with FormData sets the content-type header with a boundary that might cause issues
      const params = new URLSearchParams();
      params.append('username', email);
      params.append('password', password);

      const response = await fetch(
        `${apiUrl}/auth/signin`,
        {
          method: "POST",
          body: params,
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
        }
      );

      if (!response.ok) {
        let errorMessage = "Signin failed";
        try {
          const error = await response.json();
          errorMessage = error.detail || error.message || errorMessage;
        } catch (e) {
          // If response is not JSON, use status text
          errorMessage = response.statusText || errorMessage;
        }

        throw {
          status: response.status,
          code: "SIGNIN_ERROR",
          message: errorMessage,
          details: {},
        };
      }

      const data = await response.json();
      if (data.access_token) {
        tokenStorage.saveToken(data.access_token);
      }
      return { user: null, token: data.access_token };
    } catch (error: any) {
      // Handle network errors specifically
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw {
          status: 0,
          code: "NETWORK_ERROR",
          message: "Network error: Unable to reach the server. Please make sure the backend is running.",
          details: {},
        };
      }
      throw error;
    }
  },

  /**
   * Sign out the current user
   * Clears JWT token from storage
   */
  logout(): void {
    tokenStorage.clearToken();
  },

  /**
   * Check if user is authenticated
   * Returns true if valid token exists
   */
  isAuthenticated(): boolean {
    const token = tokenStorage.getToken();
    return !!token;
  },

  /**
   * Get stored token
   */
  getToken(): string | null {
    return tokenStorage.getToken();
  },
};
