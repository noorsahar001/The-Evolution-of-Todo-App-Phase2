# Tasks: Phase I Todo CLI Application

**Input**: Design documents from `/specs/001-todo-cli/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-commands.md, quickstart.md

**Tests**: Tests are NOT explicitly requested in the feature specification. Test tasks are omitted per Task Generation Rules.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths follow plan.md structure: src/models/, src/services/, src/cli/

---

## Phase 1: Setup

**Purpose**: Project initialization and basic structure

- [x] T001 Create project directory structure: src/, src/models/, src/services/, src/cli/, tests/, tests/unit/, tests/integration/
- [x] T002 [P] Create package marker src/__init__.py (empty file)
- [x] T003 [P] Create package marker src/models/__init__.py (empty file)
- [x] T004 [P] Create package marker src/services/__init__.py (empty file)
- [x] T005 [P] Create package marker src/cli/__init__.py (empty file)
- [x] T006 [P] Create package marker tests/__init__.py (empty file)
- [x] T007 [P] Create package marker tests/unit/__init__.py (empty file)
- [x] T008 [P] Create package marker tests/integration/__init__.py (empty file)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

- [x] T009 Create Task dataclass in src/models/task.py with fields: id (int), title (str), description (str), completed (bool)
- [x] T010 Create TaskService class in src/services/task_service.py with in-memory storage (dict) and next_id counter
- [x] T011 Implement get_task(id) method in src/services/task_service.py returning Task or None
- [x] T012 Implement get_all_tasks() method in src/services/task_service.py returning list of all Tasks

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Enable users to add tasks with title/description and view all tasks

**Independent Test**: Add 2-3 tasks, then view them. Verify IDs, titles, descriptions, and completion status (False) are displayed correctly.

### Implementation for User Story 1

- [x] T013 [US1] Implement add_task(title, description) method in src/services/task_service.py with auto-increment ID and completed=False
- [x] T014 [US1] Add title validation in add_task() - reject empty or whitespace-only titles
- [x] T015 [US1] Implement add_task command handler in src/cli/commands.py with prompts per contracts/cli-commands.md
- [x] T016 [US1] Implement view_tasks command handler in src/cli/commands.py with format: "ID: {id} | Title: {title} | Description: {description} | Completed: {True/False}"
- [x] T017 [US1] Handle "No tasks found" case in view_tasks command handler

**Checkpoint**: User Story 1 complete - can add and view tasks independently

---

## Phase 4: User Story 2 - Update Tasks (Priority: P2)

**Goal**: Enable users to modify task title and/or description by ID

**Independent Test**: Add a task, update its title, verify change in view. Update description, verify. Try updating non-existent ID.

### Implementation for User Story 2

- [x] T018 [US2] Implement update_task(id, title, description) method in src/services/task_service.py
- [x] T019 [US2] Add ID existence validation in update_task() - return False if task not found
- [x] T020 [US2] Add title validation in update_task() - reject whitespace-only titles when provided
- [x] T021 [US2] Implement update_task command handler in src/cli/commands.py with prompts per contracts/cli-commands.md
- [x] T022 [US2] Handle "Invalid task ID" and "Task title cannot be empty" error messages

**Checkpoint**: User Story 2 complete - can update tasks independently

---

## Phase 5: User Story 3 - Delete Tasks (Priority: P3)

**Goal**: Enable users to remove tasks by ID

**Independent Test**: Add a task, delete it, verify it no longer appears in view. Try deleting non-existent ID.

### Implementation for User Story 3

- [x] T023 [US3] Implement delete_task(id) method in src/services/task_service.py
- [x] T024 [US3] Add ID existence validation in delete_task() - return False if task not found
- [x] T025 [US3] Implement delete_task command handler in src/cli/commands.py with prompts per contracts/cli-commands.md
- [x] T026 [US3] Handle "Invalid task ID" error message

**Checkpoint**: User Story 3 complete - can delete tasks independently

---

## Phase 6: User Story 4 - Toggle Task Completion (Priority: P4)

**Goal**: Enable users to toggle task completion status by ID

**Independent Test**: Add a task, toggle it (expect "marked as Completed"), toggle again (expect "marked as Incomplete"), verify status in view.

### Implementation for User Story 4

- [x] T027 [US4] Implement toggle_task(id) method in src/services/task_service.py returning new status or None
- [x] T028 [US4] Add ID existence validation in toggle_task() - return None if task not found
- [x] T029 [US4] Implement toggle_task command handler in src/cli/commands.py with prompts per contracts/cli-commands.md
- [x] T030 [US4] Handle "Task {id} marked as Completed" and "Task {id} marked as Incomplete" messages based on new status
- [x] T031 [US4] Handle "Invalid task ID" error message

**Checkpoint**: User Story 4 complete - can toggle task completion independently

---

## Phase 7: User Story 5 - CLI Menu Navigation (Priority: P5)

**Goal**: Provide a menu interface for command selection

**Independent Test**: Run application, verify menu displays all 6 options, select each option, verify correct command executes, exit cleanly.

### Implementation for User Story 5

- [x] T032 [US5] Create display_menu() function in src/cli/menu.py showing all options per contracts/cli-commands.md
- [x] T033 [US5] Create get_user_choice() function in src/cli/menu.py with input validation
- [x] T034 [US5] Handle invalid menu option with "Invalid option. Please try again." message
- [x] T035 [US5] Create main loop in src/main.py that displays menu, gets choice, dispatches to command handlers
- [x] T036 [US5] Implement exit option (choice "6") with "Goodbye!" message
- [x] T037 [US5] Add keyboard interrupt handling (Ctrl+C) for graceful exit

**Checkpoint**: User Story 5 complete - full CLI menu navigation working

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Error handling improvements and final validation

- [x] T038 Add try/except wrapper in src/main.py main loop to prevent crashes on any exception
- [x] T039 Validate all error messages match specification exactly per contracts/cli-commands.md
- [x] T040 Run quickstart.md validation checklist manually

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in priority order (P1 → P2 → P3 → P4 → P5)
  - User stories can also run in parallel if staffed
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational - Uses Task model from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational - Uses Task model from US1 but independently testable
- **User Story 4 (P4)**: Can start after Foundational - Uses Task model from US1 but independently testable
- **User Story 5 (P5)**: Requires all command handlers (US1-US4) for menu dispatch

### Within Each User Story

- Service methods before command handlers
- Validation logic within service methods
- Error handling in command handlers

### Parallel Opportunities

- All Setup tasks T002-T008 can run in parallel
- User Stories 1-4 can run in parallel (if multiple developers)
- Within each story, service tasks complete before CLI tasks

---

## Parallel Execution Examples

### Setup Phase (Phase 1)

```bash
# After T001 creates directories, all package markers can run in parallel:
Task T002: Create src/__init__.py
Task T003: Create src/models/__init__.py
Task T004: Create src/services/__init__.py
Task T005: Create src/cli/__init__.py
Task T006: Create tests/__init__.py
Task T007: Create tests/unit/__init__.py
Task T008: Create tests/integration/__init__.py
```

### User Story 1 (Phase 3)

```bash
# Service tasks must complete before CLI tasks:
Task T013: add_task service method
Task T014: title validation (depends on T013)
Task T015: add_task CLI handler (depends on T013, T014)
Task T016: view_tasks CLI handler (depends on T012)
Task T017: "No tasks found" handling (depends on T016)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test add and view independently
5. MVP ready for demo

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Demo (MVP!)
3. Add User Story 2 → Test independently → Demo
4. Add User Story 3 → Test independently → Demo
5. Add User Story 4 → Test independently → Demo
6. Add User Story 5 → Test independently → Demo (Full feature)
7. Polish → Final validation

### Single Developer Strategy

Execute phases in order:
1. Setup (T001-T008)
2. Foundational (T009-T012)
3. User Story 1 (T013-T017)
4. User Story 2 (T018-T022)
5. User Story 3 (T023-T026)
6. User Story 4 (T027-T031)
7. User Story 5 (T032-T037)
8. Polish (T038-T040)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Tests omitted per specification - no TDD requested

## Implementation Complete

**Status**: All 40 tasks completed
**Date**: 2025-12-26
