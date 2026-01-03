"use client";

import { useState, useEffect } from "react";
import type { Task, TaskCreate, TaskUpdate } from "@/types";

/**
 * Task form for creating and editing tasks.
 *
 * Per FR-027, US4, US5, T081: Create/edit task form with title, description.
 * Per FR-028, T087: Validation error for empty title.
 */
interface TaskFormProps {
  task?: Task | null;
  onSubmit: (data: TaskCreate | TaskUpdate) => Promise<void>;
  onCancel: () => void;
  isLoading?: boolean;
}

export function TaskForm({ task, onSubmit, onCancel, isLoading }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || "");
  const [description, setDescription] = useState(task?.description || "");
  const [error, setError] = useState<string | null>(null);

  const isEditing = !!task;

  // Reset form when task changes
  useEffect(() => {
    setTitle(task?.title || "");
    setDescription(task?.description || "");
    setError(null);
  }, [task]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Client-side validation
    if (!title.trim()) {
      setError("Title is required");
      return;
    }

    try {
      await onSubmit({
        title: title.trim(),
        description: description.trim() || null,
      });
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="rounded-lg border bg-white p-4 shadow-sm">
      <h2 className="mb-4 text-lg font-semibold text-gray-900">
        {isEditing ? "Edit Task" : "Create New Task"}
      </h2>

      {error && (
        <div className="mb-4 rounded-md bg-red-50 p-3">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div className="space-y-4">
        <div>
          <label
            htmlFor="title"
            className="block text-sm font-medium text-gray-700"
          >
            Title <span className="text-red-500">*</span>
          </label>
          <input
            id="title"
            type="text"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="What needs to be done?"
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            disabled={isLoading}
            autoFocus
          />
        </div>

        <div>
          <label
            htmlFor="description"
            className="block text-sm font-medium text-gray-700"
          >
            Description
          </label>
          <textarea
            id="description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Add more details (optional)"
            rows={3}
            className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:outline-none focus:ring-1 focus:ring-blue-500"
            disabled={isLoading}
          />
        </div>
      </div>

      <div className="mt-4 flex justify-end gap-3">
        <button
          type="button"
          onClick={onCancel}
          disabled={isLoading}
          className="rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isLoading}
          className="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
        >
          {isLoading
            ? isEditing
              ? "Saving..."
              : "Creating..."
            : isEditing
            ? "Save Changes"
            : "Create Task"}
        </button>
      </div>
    </form>
  );
}
