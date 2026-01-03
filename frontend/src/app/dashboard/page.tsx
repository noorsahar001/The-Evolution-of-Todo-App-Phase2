"use client";

import { useState, useEffect, useCallback } from "react";
import { useRouter } from "next/navigation";
import type { Task, TaskCreate, TaskUpdate } from "@/types";
import {
  getTasks,
  createTask,
  updateTask,
  deleteTask,
  toggleTask,
  ApiError,
} from "@/lib/api";
import { TaskList } from "@/components/tasks/TaskList";
import { TaskForm } from "@/components/tasks/TaskForm";
import { DeleteConfirm } from "@/components/tasks/DeleteConfirm";

/**
 * Dashboard page for task management.
 *
 * Per FR-026, US3, T073: Task dashboard page.
 * Per T083: Fetch and display tasks on load.
 * Per T086, T088, T089: Create, edit, delete task flows.
 * Per T091: Loading states during API calls.
 * Per T092: Handle and display API errors.
 */
export default function DashboardPage() {
  const router = useRouter();

  // State
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [showForm, setShowForm] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  // Delete state
  const [deletingTask, setDeletingTask] = useState<Task | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);

  // Loading state for individual task operations
  const [loadingTaskId, setLoadingTaskId] = useState<number | null>(null);

  // Fetch tasks
  const fetchTasks = useCallback(async () => {
    try {
      setError(null);
      const data = await getTasks();
      setTasks(data);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        // Redirect to login if unauthorized
        router.push("/login");
        return;
      }
      setError(err instanceof Error ? err.message : "Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  }, [router]);

  // Load tasks on mount
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  // Handle create task
  const handleCreate = async (data: TaskCreate | TaskUpdate) => {
    setIsSubmitting(true);
    try {
      const newTask = await createTask(data as TaskCreate);
      setTasks((prev) => [newTask, ...prev]);
      setShowForm(false);
    } catch (err) {
      throw err; // Let the form handle the error
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle update task
  const handleUpdate = async (data: TaskCreate | TaskUpdate) => {
    if (!editingTask) return;

    setIsSubmitting(true);
    try {
      const updatedTask = await updateTask(editingTask.id, data as TaskUpdate);
      setTasks((prev) =>
        prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
      );
      setEditingTask(null);
    } catch (err) {
      throw err; // Let the form handle the error
    } finally {
      setIsSubmitting(false);
    }
  };

  // Handle toggle task
  const handleToggle = async (id: number) => {
    setLoadingTaskId(id);
    try {
      const updatedTask = await toggleTask(id);
      setTasks((prev) =>
        prev.map((t) => (t.id === updatedTask.id ? updatedTask : t))
      );
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        router.push("/login");
        return;
      }
      setError(err instanceof Error ? err.message : "Failed to toggle task");
    } finally {
      setLoadingTaskId(null);
    }
  };

  // Handle delete task
  const handleDelete = async () => {
    if (!deletingTask) return;

    setIsDeleting(true);
    try {
      await deleteTask(deletingTask.id);
      setTasks((prev) => prev.filter((t) => t.id !== deletingTask.id));
      setDeletingTask(null);
    } catch (err) {
      if (err instanceof ApiError && err.status === 401) {
        router.push("/login");
        return;
      }
      setError(err instanceof Error ? err.message : "Failed to delete task");
    } finally {
      setIsDeleting(false);
    }
  };

  // Cancel form
  const handleCancel = () => {
    setShowForm(false);
    setEditingTask(null);
  };

  // Open edit form
  const handleEdit = (task: Task) => {
    setEditingTask(task);
    setShowForm(false);
  };

  // Open delete confirm
  const handleDeleteClick = (task: Task) => {
    setDeletingTask(task);
  };

  // Loading state
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="h-8 w-8 animate-spin rounded-full border-4 border-blue-600 border-t-transparent" />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Error display */}
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <div className="flex">
            <div className="shrink-0">
              <svg
                className="h-5 w-5 text-red-400"
                viewBox="0 0 20 20"
                fill="currentColor"
              >
                <path
                  fillRule="evenodd"
                  d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                  clipRule="evenodd"
                />
              </svg>
            </div>
            <div className="ml-3">
              <p className="text-sm text-red-700">{error}</p>
            </div>
            <div className="ml-auto pl-3">
              <button
                onClick={() => setError(null)}
                className="inline-flex rounded-md p-1.5 text-red-500 hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2"
              >
                <span className="sr-only">Dismiss</span>
                <svg className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path
                    fillRule="evenodd"
                    d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                    clipRule="evenodd"
                  />
                </svg>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Create task button or form */}
      {!showForm && !editingTask && (
        <button
          onClick={() => setShowForm(true)}
          className="flex w-full items-center justify-center gap-2 rounded-lg border-2 border-dashed border-gray-300 bg-white p-4 text-gray-600 hover:border-blue-400 hover:text-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          <svg
            className="h-5 w-5"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 4v16m8-8H4"
            />
          </svg>
          Add New Task
        </button>
      )}

      {/* Create form */}
      {showForm && (
        <TaskForm
          onSubmit={handleCreate}
          onCancel={handleCancel}
          isLoading={isSubmitting}
        />
      )}

      {/* Edit form */}
      {editingTask && (
        <TaskForm
          task={editingTask}
          onSubmit={handleUpdate}
          onCancel={handleCancel}
          isLoading={isSubmitting}
        />
      )}

      {/* Task list */}
      <TaskList
        tasks={tasks}
        onToggle={handleToggle}
        onEdit={handleEdit}
        onDelete={handleDeleteClick}
        loadingTaskId={loadingTaskId}
      />

      {/* Delete confirmation modal */}
      {deletingTask && (
        <DeleteConfirm
          task={deletingTask}
          onConfirm={handleDelete}
          onCancel={() => setDeletingTask(null)}
          isLoading={isDeleting}
        />
      )}
    </div>
  );
}
