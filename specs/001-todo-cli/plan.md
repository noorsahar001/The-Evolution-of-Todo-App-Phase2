# Implementation Plan: Phase I Todo CLI Application

**Branch**: `001-todo-cli` | **Date**: 2025-12-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli/spec.md`

## Summary

Build a Python in-memory console-based Todo application with five core commands (add, view, update, delete, toggle) and a CLI menu interface. The application uses Python 3.13+ with standard library only, storing all tasks in memory with no persistence between runs.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (Python standard library only)
**Storage**: In-memory (Python dictionary keyed by task ID)
**Testing**: pytest (if tests are requested)
**Target Platform**: Cross-platform (Windows, macOS, Linux terminal)
**Project Type**: Single project
**Performance Goals**: Instant response (<100ms) for all operations
**Constraints**: No external dependencies, no file I/O, no network
**Scale/Scope**: Single user, single session, unlimited tasks (memory permitting)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Spec-Driven Development | All behavior defined in spec before implementation | PASS - spec.md complete |
| II. In-Scope Features | Only add, view, update, delete, toggle | PASS - spec covers exactly these |
| III. Exclusions | No DB, web, auth, AI, containers | PASS - in-memory only, CLI only |
| IV. Task Rules & Validation | Auto-increment IDs, non-empty titles, graceful errors | PASS - all in FR-001 to FR-013 |
| V. Data Storage Rules | In-memory only (list or dict) | PASS - using Python dict |
| VI. Simplicity & YAGNI | Smallest viable implementation | PASS - no unnecessary abstractions |

**Gate Status**: PASSED - All constitutional requirements satisfied.

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (CLI command contracts)
├── checklists/          # Quality checklists
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Entry point with main loop
├── models/
│   ├── __init__.py
│   └── task.py          # Task dataclass
├── services/
│   ├── __init__.py
│   └── task_service.py  # Business logic (add, update, delete, toggle, get_all)
└── cli/
    ├── __init__.py
    ├── menu.py          # Menu display and input handling
    └── commands.py      # Command handlers (add_task, view_tasks, etc.)

tests/
├── __init__.py
├── unit/
│   ├── __init__.py
│   ├── test_task.py         # Task model tests
│   └── test_task_service.py # Service tests
└── integration/
    ├── __init__.py
    └── test_cli.py          # End-to-end CLI tests
```

**Structure Decision**: Single project structure per constitution. Models, services, and CLI separated for testability. Entry point at `src/main.py`.

## Complexity Tracking

> No violations - constitution compliance verified.

| Aspect | Decision | Justification |
|--------|----------|---------------|
| Storage structure | Python dict | O(1) lookup by ID vs O(n) for list |
| Task model | dataclass | Standard library, immutable-friendly, minimal boilerplate |
| ID generation | Module-level counter | Simplest approach for single-session, single-user |
