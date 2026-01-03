/**
 * TypeScript types matching backend API schemas.
 *
 * Per spec.md: Frontend types MUST match backend schemas exactly.
 */

/**
 * User response from API (without password).
 */
export interface User {
  id: number;
  email: string;
  created_at: string;
}

/**
 * Task data from API.
 */
export interface Task {
  id: number;
  title: string;
  description: string | null;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Data for creating a new task.
 */
export interface TaskCreate {
  title: string;
  description?: string | null;
}

/**
 * Data for updating an existing task.
 */
export interface TaskUpdate {
  title?: string;
  description?: string | null;
}

/**
 * Data for user registration.
 */
export interface UserCreate {
  email: string;
  password: string;
}

/**
 * Data for user login.
 */
export interface UserLogin {
  email: string;
  password: string;
}

/**
 * API error response format.
 */
export interface ErrorResponse {
  detail: string;
}

/**
 * Error codes from API headers.
 */
export enum ErrorCode {
  VALIDATION_ERROR = "VALIDATION_ERROR",
  UNAUTHORIZED = "UNAUTHORIZED",
  FORBIDDEN = "FORBIDDEN",
  NOT_FOUND = "NOT_FOUND",
  CONFLICT = "CONFLICT",
  INTERNAL_ERROR = "INTERNAL_ERROR",
}
