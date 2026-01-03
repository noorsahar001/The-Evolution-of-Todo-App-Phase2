# Quickstart: Phase I Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2025-12-26

## Prerequisites

- Python 3.13 or higher installed
- Terminal/Console access

## Installation

No installation required. The application uses only Python standard library.

## Running the Application

```bash
# From repository root
python src/main.py
```

## Usage

When the application starts, you'll see the main menu:

```text
=== Todo App Menu ===
1. Add Task
2. View Tasks
3. Update Task
4. Delete Task
5. Toggle Task Completion
6. Exit

Enter your choice:
```

### Add a Task

1. Select option `1`
2. Enter a task title (required)
3. Enter a description (optional, press Enter to skip)

```text
Enter your choice: 1
Enter task title: Buy groceries
Enter task description (optional): Milk, eggs, bread
Task added successfully with ID 1
```

### View All Tasks

1. Select option `2`

```text
Enter your choice: 2
ID: 1 | Title: Buy groceries | Description: Milk, eggs, bread | Completed: False
```

### Update a Task

1. Select option `3`
2. Enter the task ID to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

```text
Enter your choice: 3
Enter task ID to update: 1
Enter new title (leave empty to keep current): Buy organic groceries
Enter new description (leave empty to keep current):
Task 1 updated successfully
```

### Delete a Task

1. Select option `4`
2. Enter the task ID to delete

```text
Enter your choice: 4
Enter task ID to delete: 1
Task 1 deleted successfully
```

### Toggle Task Completion

1. Select option `5`
2. Enter the task ID to toggle

```text
Enter your choice: 5
Enter task ID to toggle: 1
Task 1 marked as Completed
```

### Exit

1. Select option `6`

```text
Enter your choice: 6
Goodbye!
```

## Error Handling

The application handles errors gracefully:

```text
# Empty title
Enter task title:
Task title cannot be empty

# Invalid task ID
Enter task ID to update: 99
Invalid task ID

# Non-numeric input
Enter task ID to delete: abc
Invalid task ID
```

## Testing (if implemented)

```bash
# Run all tests
pytest tests/

# Run unit tests only
pytest tests/unit/

# Run integration tests only
pytest tests/integration/
```

## Validation Checklist

After implementation, verify:

- [ ] Add task with title only works
- [ ] Add task with title and description works
- [ ] Add task with empty title shows error
- [ ] View tasks shows all tasks
- [ ] View tasks shows "No tasks found" when empty
- [ ] Update task title works
- [ ] Update task description works
- [ ] Update with invalid ID shows error
- [ ] Delete task works
- [ ] Delete with invalid ID shows error
- [ ] Toggle changes False to True
- [ ] Toggle changes True to False
- [ ] Toggle with invalid ID shows error
- [ ] Invalid menu option shows error
- [ ] Exit terminates cleanly
