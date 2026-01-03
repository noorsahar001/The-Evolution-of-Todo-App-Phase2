from typing import Optional

from src.models.task import Task


class TaskService:
    """Service for managing tasks in memory."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID. Returns None if not found."""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks, ordered by ID."""
        return [self._tasks[task_id] for task_id in sorted(self._tasks.keys())]

    def add_task(self, title: str, description: str = "") -> tuple[bool, int | str]:
        """
        Add a new task with the given title and description.

        Returns:
            (True, task_id) on success
            (False, error_message) on validation failure
        """
        if not title or not title.strip():
            return (False, "Task title cannot be empty")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            completed=False
        )
        self._tasks[self._next_id] = task
        task_id = self._next_id
        self._next_id += 1
        return (True, task_id)

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> tuple[bool, str]:
        """
        Update a task's title and/or description.

        Returns:
            (True, success_message) on success
            (False, error_message) on failure
        """
        task = self._tasks.get(task_id)
        if task is None:
            return (False, "Invalid task ID")

        if title is not None:
            if not title.strip():
                return (False, "Task title cannot be empty")
            task.title = title.strip()

        if description is not None:
            task.description = description

        return (True, f"Task {task_id} updated successfully")

    def delete_task(self, task_id: int) -> tuple[bool, str]:
        """
        Delete a task by ID.

        Returns:
            (True, success_message) on success
            (False, error_message) if task not found
        """
        if task_id not in self._tasks:
            return (False, "Invalid task ID")

        del self._tasks[task_id]
        return (True, f"Task {task_id} deleted successfully")

    def toggle_task(self, task_id: int) -> Optional[bool]:
        """
        Toggle a task's completion status.

        Returns:
            The new completion status (True/False) on success
            None if task not found
        """
        task = self._tasks.get(task_id)
        if task is None:
            return None

        task.completed = not task.completed
        return task.completed
