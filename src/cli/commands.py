from src.services.task_service import TaskService


def add_task_command(service: TaskService) -> None:
    """Handle the add_task command."""
    title = input("Enter task title: ")

    if not title or not title.strip():
        print("Task title cannot be empty")
        return

    description = input("Enter task description (optional): ")
    success, result = service.add_task(title, description)

    if success:
        print(f"Task added successfully with ID {result}")
    else:
        print(result)


def view_tasks_command(service: TaskService) -> None:
    """Handle the view_tasks command."""
    tasks = service.get_all_tasks()
    if not tasks:
        print("No tasks found")
        return

    for task in tasks:
        print(
            f"ID: {task.id} | Title: {task.title} | "
            f"Description: {task.description} | Completed: {task.completed}"
        )


def update_task_command(service: TaskService) -> None:
    """Handle the update_task command."""
    task_id_str = input("Enter task ID to update: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID")
        return

    if service.get_task(task_id) is None:
        print("Invalid task ID")
        return

    title = input("Enter new title (leave empty to keep current): ")
    description = input("Enter new description (leave empty to keep current): ")

    new_title = title if title else None
    new_description = description if description else None

    if new_title is not None and not new_title.strip():
        print("Task title cannot be empty")
        return

    success, message = service.update_task(task_id, new_title, new_description)
    print(message)


def delete_task_command(service: TaskService) -> None:
    """Handle the delete_task command."""
    task_id_str = input("Enter task ID to delete: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID")
        return

    success, message = service.delete_task(task_id)
    print(message)


def toggle_task_command(service: TaskService) -> None:
    """Handle the toggle_task command."""
    task_id_str = input("Enter task ID to toggle: ")

    try:
        task_id = int(task_id_str)
    except ValueError:
        print("Invalid task ID")
        return

    new_status = service.toggle_task(task_id)

    if new_status is None:
        print("Invalid task ID")
    elif new_status:
        print(f"Task {task_id} marked as Completed")
    else:
        print(f"Task {task_id} marked as Incomplete")
