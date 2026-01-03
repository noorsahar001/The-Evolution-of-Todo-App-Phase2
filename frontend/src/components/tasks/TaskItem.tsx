"use client";

import type { Task } from "@/types";

/**
 * Single task item component.
 *
 * Per FR-027: Display task with toggle, edit, delete actions.
 * Per US3, T085: Visual distinction for completed tasks.
 * Per US7, T090: Toggle completion handler.
 */
interface TaskItemProps {
  task: Task;
  onToggle: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  isLoading?: boolean;
}

export function TaskItem({
  task,
  onToggle,
  onEdit,
  onDelete,
  isLoading,
}: TaskItemProps) {
  return (
    <div
      className={`rounded-lg border bg-white p-4 shadow-sm transition-opacity ${
        task.is_completed ? "bg-gray-50 opacity-75" : ""
      } ${isLoading ? "pointer-events-none opacity-50" : ""}`}
    >
      <div className="flex items-start gap-3">
        {/* Checkbox for toggle */}
        <button
          onClick={() => onToggle(task.id)}
          disabled={isLoading}
          className="mt-1 flex h-5 w-5 shrink-0 items-center justify-center rounded border border-gray-300 hover:border-blue-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          aria-label={task.is_completed ? "Mark as incomplete" : "Mark as complete"}
        >
          {task.is_completed && (
            <svg
              className="h-3 w-3 text-blue-600"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                clipRule="evenodd"
              />
            </svg>
          )}
        </button>

        {/* Task content */}
        <div className="min-w-0 flex-1">
          <h3
            className={`font-medium ${
              task.is_completed ? "text-gray-500 line-through" : "text-gray-900"
            }`}
          >
            {task.title}
          </h3>
          {task.description && (
            <p
              className={`mt-1 text-sm ${
                task.is_completed ? "text-gray-400" : "text-gray-600"
              }`}
            >
              {task.description}
            </p>
          )}
        </div>

        {/* Action buttons */}
        <div className="flex shrink-0 gap-2">
          <button
            onClick={() => onEdit(task)}
            disabled={isLoading}
            className="rounded p-1.5 text-gray-400 hover:bg-gray-100 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            aria-label="Edit task"
          >
            <svg
              className="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
              />
            </svg>
          </button>
          <button
            onClick={() => onDelete(task)}
            disabled={isLoading}
            className="rounded p-1.5 text-gray-400 hover:bg-red-50 hover:text-red-600 focus:outline-none focus:ring-2 focus:ring-red-500"
            aria-label="Delete task"
          >
            <svg
              className="h-4 w-4"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>
  );
}
