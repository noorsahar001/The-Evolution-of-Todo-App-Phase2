"use client";

import type { Task } from "@/types";
import { TaskItem } from "./TaskItem";

/**
 * Task list component.
 *
 * Per FR-026, US3, T079: Display task array or empty state.
 * Per T084: Show "No tasks yet" empty state.
 */
interface TaskListProps {
  tasks: Task[];
  onToggle: (id: number) => void;
  onEdit: (task: Task) => void;
  onDelete: (task: Task) => void;
  loadingTaskId?: number | null;
}

export function TaskList({
  tasks,
  onToggle,
  onEdit,
  onDelete,
  loadingTaskId,
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="rounded-lg border-2 border-dashed border-gray-300 bg-white p-12 text-center">
        <svg
          className="mx-auto h-12 w-12 text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            strokeLinecap="round"
            strokeLinejoin="round"
            strokeWidth={1.5}
            d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
          />
        </svg>
        <h3 className="mt-4 text-lg font-medium text-gray-900">No tasks yet</h3>
        <p className="mt-2 text-sm text-gray-500">
          Get started by creating your first task above.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onToggle={onToggle}
          onEdit={onEdit}
          onDelete={onDelete}
          isLoading={loadingTaskId === task.id}
        />
      ))}
    </div>
  );
}
