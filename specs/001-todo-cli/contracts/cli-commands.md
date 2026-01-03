# CLI Command Contracts: Phase I Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2025-12-26

## Overview

This document defines the contract for each CLI command, including inputs, outputs, and error conditions.

---

## 1. add_task

**Purpose**: Create a new task

### Input

| Field | Type | Required | Prompt |
|-------|------|----------|--------|
| title | string | Yes | "Enter task title: " |
| description | string | No | "Enter task description (optional): " |

### Output

**Success**:
```text
Task added successfully with ID {task_id}
```

**Failure**:
```text
Task title cannot be empty
```

### Behavior

1. Prompt user for title
2. Validate title is not empty/whitespace
3. If invalid, display error and return to menu
4. Prompt user for description (accept empty)
5. Create task with auto-incremented ID, completed=False
6. Display success message with new ID
7. Return to menu

---

## 2. view_tasks

**Purpose**: Display all tasks

### Input

None

### Output

**With tasks**:
```text
ID: {id} | Title: {title} | Description: {description} | Completed: {True/False}
```
(Repeated for each task, ordered by ID)

**No tasks**:
```text
No tasks found
```

### Behavior

1. Retrieve all tasks from storage
2. If empty, display "No tasks found"
3. If not empty, display each task in format above
4. Return to menu

---

## 3. update_task

**Purpose**: Modify an existing task's title and/or description

### Input

| Field | Type | Required | Prompt |
|-------|------|----------|--------|
| task_id | integer | Yes | "Enter task ID to update: " |
| title | string | No | "Enter new title (leave empty to keep current): " |
| description | string | No | "Enter new description (leave empty to keep current): " |

### Output

**Success**:
```text
Task {task_id} updated successfully
```

**Failure - Invalid ID**:
```text
Invalid task ID
```

**Failure - Empty title**:
```text
Task title cannot be empty
```

### Behavior

1. Prompt user for task ID
2. Validate ID is integer and exists
3. If invalid, display error and return to menu
4. Prompt for new title
5. If new title provided and is whitespace-only, display error and return
6. Prompt for new description
7. Update task with provided non-empty values
8. Display success message
9. Return to menu

---

## 4. delete_task

**Purpose**: Remove a task

### Input

| Field | Type | Required | Prompt |
|-------|------|----------|--------|
| task_id | integer | Yes | "Enter task ID to delete: " |

### Output

**Success**:
```text
Task {task_id} deleted successfully
```

**Failure**:
```text
Invalid task ID
```

### Behavior

1. Prompt user for task ID
2. Validate ID is integer and exists
3. If invalid, display error and return to menu
4. Remove task from storage
5. Display success message
6. Return to menu

---

## 5. toggle_task

**Purpose**: Toggle task completion status

### Input

| Field | Type | Required | Prompt |
|-------|------|----------|--------|
| task_id | integer | Yes | "Enter task ID to toggle: " |

### Output

**Success (marked complete)**:
```text
Task {task_id} marked as Completed
```

**Success (marked incomplete)**:
```text
Task {task_id} marked as Incomplete
```

**Failure**:
```text
Invalid task ID
```

### Behavior

1. Prompt user for task ID
2. Validate ID is integer and exists
3. If invalid, display error and return to menu
4. Toggle completed status (True → False or False → True)
5. Display appropriate success message based on new status
6. Return to menu

---

## 6. Main Menu

**Purpose**: Command selection interface

### Display

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

### Input

| Field | Type | Required | Prompt |
|-------|------|----------|--------|
| choice | string | Yes | "Enter your choice: " |

### Output

**Invalid choice**:
```text
Invalid option. Please try again.
```

### Behavior

1. Display menu
2. Prompt for choice
3. If valid choice (1-6), execute corresponding command
4. If choice is "6" or "exit", terminate application
5. If invalid, display error and show menu again
6. Loop until exit

---

## Error Handling Contract

All commands MUST:
- Never crash on invalid input
- Convert non-integer task IDs to "Invalid task ID" message
- Handle keyboard interrupts gracefully (exit cleanly)
- Return to menu after any operation (except exit)
