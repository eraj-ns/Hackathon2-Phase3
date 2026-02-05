/**
 * API Client Service with JWT Authentication
 * Spec-3: Frontend Application & Full-Stack Integration
 * Provides Axios instance with JWT interceptor for all API calls
 */

import axios, { AxiosInstance, AxiosError, InternalAxiosRequestConfig } from "axios";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// Create Axios instance
const apiClient: AxiosInstance = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

/**
 * Token Storage Utilities
 */
export const tokenStorage = {
  saveToken: (token: string): void => {
    if (typeof window !== "undefined") {
      localStorage.setItem("authToken", token);
    }
  },

  getToken: (): string | null => {
    if (typeof window !== "undefined") {
      return localStorage.getItem("authToken");
    }
    return null;
  },

  clearToken: (): void => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("authToken");
    }
  },
};

/**
 * Request Interceptor: Attach JWT token to all requests
 */
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = tokenStorage.getToken();
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

/**
 * Response Interceptor: Handle errors and token expiration
 */
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // Handle 401 Unauthorized (session expired)
    if (error.response?.status === 401) {
      tokenStorage.clearToken();
      if (typeof window !== "undefined") {
        window.location.href = "/signin?reason=session_expired";
      }
    }

    // Return formatted error
    return Promise.reject({
      status: error.response?.status || 500,
      code: (error.response?.data as any)?.code || "UNKNOWN_ERROR",
      message:
        (error.response?.data as any)?.message ||
        error.message ||
        "An error occurred",
      details: (error.response?.data as any)?.details || {},
    });
  }
);

export default apiClient;
