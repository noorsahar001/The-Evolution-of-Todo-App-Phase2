# Data Model: Phase I Todo CLI Application

**Feature**: 001-todo-cli
**Date**: 2025-12-26

## Entities

### Task

The core entity representing a single todo item.

| Field | Type | Required | Default | Constraints |
|-------|------|----------|---------|-------------|
| id | integer | Yes | Auto-generated | Positive, unique, auto-incrementing starting from 1 |
| title | string | Yes | - | Non-empty, not whitespace-only |
| description | string | No | "" (empty string) | Any string, including empty |
| completed | boolean | Yes | False | True or False |

#### Validation Rules

1. **id**: MUST be a positive integer, assigned automatically, never reused
2. **title**: MUST NOT be empty or consist only of whitespace
3. **description**: MAY be empty, no length restrictions for Phase I
4. **completed**: MUST be boolean, defaults to False on creation

#### State Transitions

```text
Task Creation:
  [No Task] --add_task(title, description?)--> [Task: completed=False]

Task Update:
  [Task] --update_task(id, title?, description?)--> [Task: updated fields]

Task Toggle:
  [Task: completed=False] --toggle_task(id)--> [Task: completed=True]
  [Task: completed=True] --toggle_task(id)--> [Task: completed=False]

Task Deletion:
  [Task] --delete_task(id)--> [No Task]
```

## Storage Structure

### In-Memory Store

```python
# Type: Dict[int, Task]
# Key: task.id (integer)
# Value: Task dataclass instance

tasks: Dict[int, Task] = {}
next_id: int = 1
```

### Operations Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| add_task | O(1) | O(1) |
| get_task(id) | O(1) | O(1) |
| get_all_tasks | O(n) | O(n) |
| update_task(id) | O(1) | O(1) |
| delete_task(id) | O(1) | O(1) |
| toggle_task(id) | O(1) | O(1) |

Where n = number of tasks in storage.

## Relationships

No relationships in Phase I. Task is the only entity with no foreign keys or associations.

## Display Format

Per specification, tasks are displayed as:

```text
ID: {id} | Title: {title} | Description: {description} | Completed: {True/False}
```

Example:
```text
ID: 1 | Title: Buy groceries | Description: Milk, eggs, bread | Completed: False
ID: 2 | Title: Call mom | Description: | Completed: True
```
