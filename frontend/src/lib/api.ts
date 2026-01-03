/**
 * API client for communicating with the backend.
 *
 * Per FR-006: Uses credentials:'include' to send httpOnly cookies with requests.
 * Per FR-022: Handles API errors consistently.
 */

import type {
  User,
  Task,
  TaskCreate,
  TaskUpdate,
  UserCreate,
  UserLogin,
  ErrorResponse,
} from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

/**
 * Custom error class for API errors.
 */
export class ApiError extends Error {
  constructor(
    message: string,
    public status: number,
    public errorCode?: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

/**
 * Fetch wrapper with credentials and error handling.
 *
 * Per FR-006: Include credentials for cookie-based auth.
 * Per T056: Transform API errors to user-friendly messages.
 */
async function fetchApi<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    credentials: "include", // Per FR-006: Send cookies
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
  });

  // Handle successful responses
  if (response.ok) {
    // Handle 204 No Content
    if (response.status === 204) {
      return undefined as T;
    }
    return response.json();
  }

  // Handle error responses
  const errorCode = response.headers.get("X-Error-Code") || undefined;
  let errorMessage = "An unexpected error occurred";

  try {
    const errorData: ErrorResponse = await response.json();
    errorMessage = errorData.detail || errorMessage;
  } catch {
    // If JSON parsing fails, use status text
    errorMessage = response.statusText || errorMessage;
  }

  throw new ApiError(errorMessage, response.status, errorCode);
}

// =============================================================================
// Auth API
// =============================================================================

/**
 * Register a new user.
 * Per US1, FR-001 to FR-003.
 */
export async function register(data: UserCreate): Promise<User> {
  return fetchApi<User>("/api/auth/register", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Login user and set auth cookie.
 * Per US2, FR-004 to FR-006.
 */
export async function login(data: UserLogin): Promise<User> {
  return fetchApi<User>("/api/auth/login", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Logout user and clear auth cookie.
 * Per FR-007.
 */
export async function logout(): Promise<void> {
  await fetchApi<{ message: string }>("/api/auth/logout", {
    method: "POST",
  });
}

// =============================================================================
// Tasks API
// =============================================================================

/**
 * Get all tasks for the current user.
 * Per US3, FR-011, FR-017.
 */
export async function getTasks(): Promise<Task[]> {
  return fetchApi<Task[]>("/api/tasks");
}

/**
 * Get a single task by ID.
 * Per FR-011, FR-017.
 */
export async function getTask(id: number): Promise<Task> {
  return fetchApi<Task>(`/api/tasks/${id}`);
}

/**
 * Create a new task.
 * Per US4, FR-009, FR-010, FR-015, FR-016, FR-017.
 */
export async function createTask(data: TaskCreate): Promise<Task> {
  return fetchApi<Task>("/api/tasks", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

/**
 * Update an existing task.
 * Per US5, FR-012, FR-017.
 */
export async function updateTask(id: number, data: TaskUpdate): Promise<Task> {
  return fetchApi<Task>(`/api/tasks/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

/**
 * Delete a task.
 * Per US6, FR-013, FR-017.
 */
export async function deleteTask(id: number): Promise<void> {
  await fetchApi<void>(`/api/tasks/${id}`, {
    method: "DELETE",
  });
}

/**
 * Toggle task completion status.
 * Per US7, FR-014, FR-017.
 */
export async function toggleTask(id: number): Promise<Task> {
  return fetchApi<Task>(`/api/tasks/${id}/toggle`, {
    method: "PATCH",
  });
}
