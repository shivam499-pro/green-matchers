/**
 * Green Matchers Shared API Client
 * Shared between Web and Mobile applications
 */

import axios, { AxiosInstance, AxiosRequestConfig, AxiosResponse } from 'axios';

// Default API configuration
const DEFAULT_API_BASE_URL = 'http://localhost:8000';
const PRODUCTION_API_BASE_URL = 'https://api.greenmatchers.com';

interface ApiClientConfig {
  baseURL?: string;
  timeout?: number;
  headers?: Record<string, string>;
}

class ApiClient {
  private instance: AxiosInstance;
  private token: string | null = null;

  constructor(config: ApiClientConfig = {}) {
    this.instance = axios.create({
      baseURL: config.baseURL || DEFAULT_API_BASE_URL,
      timeout: config.timeout || 30000,
      headers: {
        'Content-Type': 'application/json',
        ...config.headers,
      },
    });

    // Add request interceptor for authentication
    this.instance.interceptors.request.use(
      (config) => {
        if (this.token) {
          config.headers.Authorization = `Bearer ${this.token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    // Add response interceptor for error handling
    this.instance.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response) {
          // Server responded with error status
          return Promise.reject({
            ...error,
            message: error.response.data?.error || 'Server error',
            status: error.response.status,
          });
        } else if (error.request) {
          // Request was made but no response received
          return Promise.reject({
            ...error,
            message: 'No response from server. Please check your connection.',
          });
        } else {
          // Something happened in setting up the request
          return Promise.reject({
            ...error,
            message: 'Request setup error: ' + error.message,
          });
        }
      }
    );
  }

  /**
   * Set authentication token
   * @param token JWT token
   */
  setToken(token: string | null): void {
    this.token = token;
  }

  /**
   * Clear authentication token
   */
  clearToken(): void {
    this.token = null;
  }

  /**
   * GET request
   */
  async get<T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.get<T>(url, config);
  }

  /**
   * POST request
   */
  async post<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.post<T>(url, data, config);
  }

  /**
   * PUT request
   */
  async put<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.put<T>(url, data, config);
  }

  /**
   * DELETE request
   */
  async delete<T>(url: string, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.delete<T>(url, config);
  }

  /**
   * PATCH request
   */
  async patch<T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<AxiosResponse<T>> {
    return this.instance.patch<T>(url, data, config);
  }
}

// Singleton instance for convenience
const apiClient = new ApiClient();

export { ApiClient, apiClient, DEFAULT_API_BASE_URL, PRODUCTION_API_BASE_URL };

// Export API endpoints as constants
export const API_ENDPOINTS = {
  // Authentication
  REGISTER: '/api/auth/register',
  LOGIN: '/api/auth/login',

  // Career Services
  CAREER_RECOMMENDATIONS: '/api/career/recommendations',
  CAREER_PATH: '/api/career/progression',

  // Job Services
  JOB_SEARCH: '/api/jobs/search',
  JOB_APPLY: '/api/jobs/apply',
  JOB_APPLICATIONS: '/api/users/applications',

  // Vector AI Services
  VECTOR_JOB_SEARCH: '/api/vector/jobs/search',
  VECTOR_CAREER_RECOMMEND: '/api/vector/careers/recommend',

  // Translation Services
  TRANSLATE: '/api/translate',
  LANGUAGES: '/api/languages',

  // User Services
  USER_PROFILE: '/api/users/profile',
  UPDATE_PROFILE: '/api/users/profile',
  UPLOAD_RESUME: '/api/users/upload-resume',

  // System Services
  HEALTH_CHECK: '/health',
  STATS: '/stats',
};

// Export types for better TypeScript support
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
  status?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

// Helper function to handle API errors consistently
export function handleApiError(error: any): { success: false; error: string; status?: number } {
  if (error.response) {
    return {
      success: false,
      error: error.response.data?.error || 'Server error occurred',
      status: error.response.status,
    };
  } else if (error.message) {
    return {
      success: false,
      error: error.message,
    };
  } else {
    return {
      success: false,
      error: 'Unknown error occurred',
    };
  }
}