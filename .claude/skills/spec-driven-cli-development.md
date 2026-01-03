# Skill: Spec-Driven CLI Application Development

A comprehensive skill for building CLI applications using the Spec-Driven Development (SDD) methodology.

---

## 1. Spec-Driven Development (Basics)

### Overview
Spec-Driven Development is a methodology where specifications drive the entire development lifecycle. Every feature, component, and behavior is defined upfront in structured documents before implementation begins.

### Core Workflow
```
Constitution → Specification → Plan → Tasks → Implementation → Validation
```

---

## 2. Writing sp.constitution.md

### Purpose
The constitution defines the foundational principles, constraints, and non-negotiables for the project.

### Structure
```markdown
# Project Constitution

## Project Identity
- **Name**: [Project Name]
- **Purpose**: [One-line purpose statement]
- **Target Users**: [Primary audience]

## Core Principles
1. [Principle 1 - e.g., "Simplicity over complexity"]
2. [Principle 2 - e.g., "Test-first development"]
3. [Principle 3 - e.g., "No external dependencies for core features"]

## Technical Constraints
- **Language**: [e.g., Python 3.10+]
- **Dependencies**: [Allowed/restricted libraries]
- **Data Storage**: [e.g., In-memory, file-based, database]

## Quality Standards
- **Code Coverage**: [e.g., Minimum 80%]
- **Documentation**: [Requirements]
- **Error Handling**: [Standards]

## Non-Goals
- [What this project will NOT do]
```

### Best Practices
- Keep principles measurable and actionable
- Define clear boundaries (in-scope vs out-of-scope)
- Include rationale for each constraint

---

## 3. Writing Clear sp.specify.md

### Purpose
Specifications define WHAT the feature does, not HOW it's implemented.

### Structure
```markdown
# Feature Specification: [Feature Name]

## Overview
[2-3 sentence description of the feature]

## User Stories
- As a [user], I want to [action] so that [benefit]

## Functional Requirements
### FR-001: [Requirement Name]
- **Description**: [What it does]
- **Input**: [Expected inputs]
- **Output**: [Expected outputs]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]
  - [ ] [Criterion 2]

## Non-Functional Requirements
- **Performance**: [Constraints]
- **Usability**: [Standards]

## Error Scenarios
| Error Code | Condition | User Message |
|------------|-----------|--------------|
| E001       | [When]    | [Message]    |

## Examples
### Example 1: [Scenario Name]
**Input**: [input]
**Expected Output**: [output]
```

### Best Practices
- Use concrete examples for every requirement
- Define error cases explicitly
- Keep requirements atomic and testable

---

## 4. Planning via sp.plan.md

### Purpose
The plan defines HOW the specification will be implemented architecturally.

### Structure
```markdown
# Implementation Plan: [Feature Name]

## Architecture Overview
[High-level design diagram or description]

## Components
### Component 1: [Name]
- **Responsibility**: [Single responsibility]
- **Interface**: [Public methods/functions]
- **Dependencies**: [What it needs]

## Data Structures
```python
@dataclass
class ModelName:
    field1: type
    field2: type
```

## API/Interface Design
### Command: [command-name]
- **Syntax**: `command [options] <arguments>`
- **Options**: [List of flags]
- **Returns**: [Output format]

## Implementation Approach
1. [Step 1]
2. [Step 2]
3. [Step 3]

## Technical Decisions
| Decision | Options Considered | Choice | Rationale |
|----------|-------------------|--------|-----------|
| [Topic]  | A, B, C           | B      | [Why]     |

## Risk Mitigation
- **Risk**: [Description]
- **Mitigation**: [Strategy]
```

### Best Practices
- Keep components loosely coupled
- Define clear interfaces between modules
- Document architectural decisions with rationale

---

## 5. Task Breakdown with sp.task.md

### Purpose
Break the plan into small, testable, dependency-ordered tasks.

### Structure
```markdown
# Tasks: [Feature Name]

## Task Overview
- **Total Tasks**: [N]
- **Estimated Complexity**: [Low/Medium/High]

## Tasks

### Task 1: [Task Title]
- **ID**: T-001
- **Description**: [What to implement]
- **Dependencies**: [None | T-XXX]
- **Files**: [Files to create/modify]
- **Test Cases**:
  - [ ] [Test case 1]
  - [ ] [Test case 2]
- **Acceptance Criteria**:
  - [ ] [Criterion 1]

### Task 2: [Task Title]
- **ID**: T-002
- **Dependencies**: [T-001]
...

## Task Dependency Graph
```
T-001 → T-002 → T-004
          ↓
        T-003 → T-005
```

## Definition of Done
- [ ] All tests pass
- [ ] Code reviewed
- [ ] Documentation updated
```

### Best Practices
- Each task should be completable in 1-2 hours
- Include specific test cases for each task
- Order tasks by dependencies
- Make tasks independently verifiable

---

## 6. Claude Code Based Implementation (sp.implement.md)

### Purpose
Guide the AI-assisted implementation process.

### Implementation Workflow
```markdown
# Implementation Guide

## Pre-Implementation Checklist
- [ ] Constitution reviewed
- [ ] Specification understood
- [ ] Plan approved
- [ ] Tasks prioritized

## Implementation Protocol

### For Each Task:
1. **Read**: Review task requirements and dependencies
2. **Test First**: Write failing test cases
3. **Implement**: Write minimal code to pass tests
4. **Refactor**: Clean up while keeping tests green
5. **Validate**: Run full test suite
6. **Document**: Update inline documentation

## Code Generation Prompts
### Creating a new module:
"Implement [module] following the plan in sp.plan.md,
ensuring it passes the test cases defined in T-XXX"

### Adding a feature:
"Add [feature] to [module] per FR-XXX in sp.specify.md,
with error handling for scenarios E-XXX"

## Validation Commands
```bash
# Run tests
python -m pytest tests/ -v

# Check coverage
python -m pytest --cov=src tests/

# Lint code
python -m flake8 src/
```
```

---

## 7. CLI Application Design

### Command Structure
```
app <command> [subcommand] [options] [arguments]
```

### Design Patterns

#### Command Pattern
```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self, args: list) -> str:
        pass

class AddCommand(Command):
    def execute(self, args: list) -> str:
        # Implementation
        pass
```

#### Registry Pattern
```python
class CommandRegistry:
    def __init__(self):
        self._commands: dict[str, Command] = {}

    def register(self, name: str, command: Command):
        self._commands[name] = command

    def get(self, name: str) -> Command | None:
        return self._commands.get(name)
```

### CLI Best Practices
- Provide `--help` for every command
- Use consistent option naming (`-v`/`--verbose`)
- Return meaningful exit codes (0=success, 1=error)
- Support both interactive and scriptable modes

---

## 8. In-Memory Data Handling

### Data Store Pattern
```python
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Item:
    id: int
    name: str
    completed: bool = False

class InMemoryStore:
    def __init__(self):
        self._items: dict[int, Item] = {}
        self._next_id: int = 1

    def add(self, name: str) -> Item:
        item = Item(id=self._next_id, name=name)
        self._items[self._next_id] = item
        self._next_id += 1
        return item

    def get(self, id: int) -> Optional[Item]:
        return self._items.get(id)

    def get_all(self) -> list[Item]:
        return list(self._items.values())

    def update(self, id: int, **kwargs) -> Optional[Item]:
        if item := self._items.get(id):
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            return item
        return None

    def delete(self, id: int) -> bool:
        if id in self._items:
            del self._items[id]
            return True
        return False
```

### Best Practices
- Use dataclasses for structured data
- Implement CRUD operations consistently
- Consider thread safety if needed
- Provide clear query interfaces

---

## 9. Validation & Error Handling

### Input Validation
```python
from enum import Enum

class ValidationError(Exception):
    def __init__(self, message: str, code: str):
        self.message = message
        self.code = code
        super().__init__(message)

class ErrorCode(Enum):
    INVALID_INPUT = "E001"
    NOT_FOUND = "E002"
    DUPLICATE = "E003"

def validate_task_name(name: str) -> str:
    if not name or not name.strip():
        raise ValidationError(
            "Task name cannot be empty",
            ErrorCode.INVALID_INPUT.value
        )
    if len(name) > 100:
        raise ValidationError(
            "Task name cannot exceed 100 characters",
            ErrorCode.INVALID_INPUT.value
        )
    return name.strip()
```

### Error Handling Strategy
```python
import sys

def handle_error(error: Exception) -> int:
    """Central error handler returning exit code."""
    if isinstance(error, ValidationError):
        print(f"Error [{error.code}]: {error.message}", file=sys.stderr)
        return 1
    elif isinstance(error, KeyboardInterrupt):
        print("\nOperation cancelled.", file=sys.stderr)
        return 130
    else:
        print(f"Unexpected error: {error}", file=sys.stderr)
        return 1
```

### Best Practices
- Validate at system boundaries (user input, external APIs)
- Use typed exceptions with error codes
- Provide user-friendly error messages
- Log technical details, show friendly messages

---

## 10. Spec ↔ Implementation Alignment

### Traceability Matrix
```markdown
| Requirement | Task | Test | Implementation |
|-------------|------|------|----------------|
| FR-001      | T-001| test_add_task | src/commands/add.py |
| FR-002      | T-002| test_list_tasks | src/commands/list.py |
```

### Alignment Checklist
- [ ] Every FR has at least one task
- [ ] Every task has test cases
- [ ] Every error scenario has handling code
- [ ] Every example in spec has a corresponding test

### Validation Process
```python
def validate_spec_alignment():
    """Verify implementation matches specification."""
    # 1. Parse spec requirements
    requirements = parse_spec("sp.specify.md")

    # 2. Parse implemented tests
    tests = discover_tests("tests/")

    # 3. Check coverage
    for req in requirements:
        if not any(req.id in test.docstring for test in tests):
            print(f"WARNING: {req.id} has no test coverage")
```

### Continuous Alignment
1. **Before Implementation**: Review spec requirements
2. **During Implementation**: Reference spec in code comments
3. **After Implementation**: Run traceability check
4. **On Changes**: Update spec if implementation diverges

---

## Quick Reference

### SDD Commands
| Command | Purpose |
|---------|---------|
| `/sp.constitution` | Create/update project principles |
| `/sp.specify` | Write feature specification |
| `/sp.plan` | Design implementation architecture |
| `/sp.tasks` | Break down into testable tasks |
| `/sp.implement` | Execute implementation |
| `/sp.analyze` | Validate spec alignment |

### CLI Development Checklist
- [ ] Commands follow consistent syntax
- [ ] Help text available for all commands
- [ ] Input validation at entry points
- [ ] Meaningful error messages
- [ ] Exit codes follow conventions
- [ ] In-memory store with CRUD operations
- [ ] Tests cover all spec requirements
