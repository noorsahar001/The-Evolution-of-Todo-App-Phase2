# Skill: AI-Powered Application Development with Agents

A comprehensive skill for building AI-native applications using agent architectures, tool-calling patterns, and multi-agent coordination with Spec-Driven Development.

---

## 1. AI-Native Application Design

### Overview
AI-native applications are designed from the ground up to leverage LLMs as core components, not just add-ons. The AI is a first-class citizen in the architecture.

### AI-Native vs AI-Enhanced
```
Traditional App          AI-Enhanced App         AI-Native App
┌─────────────┐          ┌─────────────┐         ┌─────────────┐
│   UI Layer  │          │   UI Layer  │         │ Conversational│
├─────────────┤          ├─────────────┤         │   Interface   │
│ App Logic   │          │ App Logic   │         ├─────────────┤
├─────────────┤          ├─────────────┤         │  AI Agent    │
│  Database   │          │ AI Feature  │         │  Orchestrator │
└─────────────┘          ├─────────────┤         ├─────────────┤
                         │  Database   │         │ Tools + MCP  │
                         └─────────────┘         ├─────────────┤
                                                 │  Database   │
                                                 └─────────────┘
```

### Architecture Principles

#### 1. Intent-Driven Interaction
```markdown
User Input → Intent Recognition → Tool Selection → Execution → Response
```

#### 2. Tool-First Design
Design capabilities as discrete, composable tools before UI.

#### 3. Context as State
Conversation history becomes application state.

#### 4. Graceful Degradation
AI failures should fall back to deterministic behavior.

### AI-Native Specification Template
```markdown
# AI Feature Specification: [Feature Name]

## Overview
[Description of AI-powered capability]

## User Intents
| Intent | Example Utterances | Expected Behavior |
|--------|-------------------|-------------------|
| create_task | "Add buy milk", "Create a task for..." | Create new task |
| list_tasks | "Show my tasks", "What do I need to do?" | Display task list |
| complete_task | "Mark task 1 done", "I finished..." | Update task status |

## AI Behavior Rules
1. [Rule 1 - e.g., "Always confirm destructive actions"]
2. [Rule 2 - e.g., "Ask for clarification if intent unclear"]
3. [Rule 3 - e.g., "Provide actionable suggestions"]

## Tool Requirements
- `add_task`: Create new task
- `list_tasks`: Retrieve tasks with filters
- `update_task`: Modify existing task
- `delete_task`: Remove task (with confirmation)

## Conversation Examples
### Example 1: Task Creation
User: "Remind me to call mom tomorrow"
AI: "I've created a task 'Call mom' for tomorrow. Would you like to set a specific time?"

### Example 2: Ambiguous Request
User: "Delete everything"
AI: "I want to make sure I understand. Do you want to delete all tasks? This cannot be undone."

## Error Handling
| Scenario | AI Response |
|----------|-------------|
| Tool failure | "I couldn't complete that action. Let me try again." |
| Ambiguous input | "I'm not sure what you mean. Did you want to [A] or [B]?" |
| Out of scope | "I can help with task management. For [X], you might try..." |
```

---

## 2. Conversational UX via Specs

### Conversation Design Document
```markdown
# Conversational UX Specification

## Persona
- **Name**: [Assistant Name]
- **Tone**: [Professional, friendly, concise]
- **Personality Traits**: [Helpful, proactive, clear]

## Conversation Principles
1. **Clarity First**: Use simple, unambiguous language
2. **Progressive Disclosure**: Start simple, offer details on request
3. **Confirmation for Risk**: Always confirm destructive actions
4. **Context Awareness**: Reference previous messages naturally

## Response Patterns

### Success Responses
```
[Action completed] + [Brief confirmation] + [Optional next step]
Example: "Done! Task 'Buy groceries' created. Need to add more?"
```

### Error Responses
```
[Acknowledgment] + [What went wrong] + [How to fix]
Example: "I couldn't find that task. Try 'list tasks' to see available tasks."
```

### Clarification Requests
```
[Acknowledge ambiguity] + [Options] + [Question]
Example: "I found 3 tasks matching 'call'. Which one: 1) Call mom 2) Call bank 3) Call doctor?"
```

## Turn-Taking Rules
- Respond within one conversational turn when possible
- Ask maximum 1 clarifying question per turn
- Provide escape options ("or say 'cancel' to stop")
```

### Intent Recognition Specification
```markdown
## Intent Taxonomy

### Primary Intents
| Intent ID | Description | Required Slots | Optional Slots |
|-----------|-------------|----------------|----------------|
| CREATE_TASK | Create new task | title | description, due_date |
| LIST_TASKS | View tasks | - | status, limit |
| UPDATE_TASK | Modify task | task_id | title, description, status |
| DELETE_TASK | Remove task | task_id | - |
| COMPLETE_TASK | Mark done | task_id | - |

### Slot Definitions
| Slot | Type | Extraction Pattern | Examples |
|------|------|-------------------|----------|
| title | string | Noun phrase after action verb | "buy milk", "call doctor" |
| task_id | integer | Number reference | "task 1", "#5", "the first one" |
| due_date | datetime | Temporal expression | "tomorrow", "next Monday", "in 2 hours" |
| status | enum | Status keywords | "done", "pending", "completed" |

### Intent Detection Examples
| User Input | Intent | Extracted Slots |
|------------|--------|-----------------|
| "Add buy groceries" | CREATE_TASK | title: "buy groceries" |
| "Show me what's left" | LIST_TASKS | status: "pending" |
| "Mark #3 as done" | COMPLETE_TASK | task_id: 3 |
| "Delete the first task" | DELETE_TASK | task_id: 1 |
```

### Conversation Flow Diagram
```
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Parse Input │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
        │ Clear     │ │Ambiguous│ │ Unknown   │
        │ Intent    │ │ Intent  │ │ Intent    │
        └─────┬─────┘ └────┬────┘ └─────┬─────┘
              │            │            │
        ┌─────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
        │ Execute   │ │ Clarify │ │ Fallback  │
        │ Tool      │ │ Request │ │ Response  │
        └─────┬─────┘ └────┬────┘ └─────┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │  Respond    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ Await Input │
                    └─────────────┘
```

---

## 3. Tool-Calling Architecture (MCP)

### Model Context Protocol Overview
MCP provides a standardized way for AI applications to connect with external tools and data sources.

```
┌─────────────────────────────────────────────────────────┐
│                    MCP Architecture                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Client    │───▶│  Protocol   │───▶│   Server    │ │
│  │  (Claude)   │◀───│   Layer     │◀───│  (Tools)    │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│                                                          │
│  Capabilities:                                          │
│  • Tools (functions the AI can call)                    │
│  • Resources (data the AI can read)                     │
│  • Prompts (templates for interactions)                 │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### MCP Tool Specification
```markdown
# MCP Tool Specification: Task Management

## Tool Definitions

### add_task
**Description**: Create a new task for the user

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| title | string | Yes | Task title (1-200 chars) |
| description | string | No | Detailed description |
| due_date | string | No | ISO 8601 datetime |

**Returns**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "description": null,
  "completed": false,
  "created_at": "2024-01-15T10:30:00Z"
}
```

**Errors**:
| Code | Condition | Message |
|------|-----------|---------|
| VALIDATION_ERROR | Empty title | "Title cannot be empty" |
| RATE_LIMIT | Too many requests | "Please wait before adding more tasks" |

### list_tasks
**Description**: Retrieve user's tasks with optional filters

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| status | enum | No | "all", "pending", "completed" |
| limit | integer | No | Max results (default: 50) |

**Returns**:
```json
{
  "tasks": [...],
  "total": 10,
  "has_more": false
}
```

### complete_task
**Description**: Mark a task as completed

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | integer | Yes | ID of task to complete |

**Returns**:
```json
{
  "id": 1,
  "title": "Buy groceries",
  "completed": true,
  "completed_at": "2024-01-15T14:30:00Z"
}
```

### delete_task
**Description**: Permanently delete a task

**Parameters**:
| Name | Type | Required | Description |
|------|------|----------|-------------|
| task_id | integer | Yes | ID of task to delete |
| confirm | boolean | Yes | Must be true |

**Returns**:
```json
{
  "deleted": true,
  "task_id": 1
}
```
```

### MCP Server Implementation (Python)
```python
# mcp_server/tools.py
from mcp.server import Server
from mcp.types import Tool, TextContent
from pydantic import BaseModel, Field
from typing import Optional
import json

# Initialize MCP server
server = Server("task-manager")

# Tool parameter schemas
class AddTaskParams(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    due_date: Optional[str] = None

class ListTasksParams(BaseModel):
    status: Optional[str] = "all"
    limit: int = Field(default=50, le=100)

class CompleteTaskParams(BaseModel):
    task_id: int

class DeleteTaskParams(BaseModel):
    task_id: int
    confirm: bool

# Register tools
@server.tool()
async def add_task(params: AddTaskParams) -> dict:
    """Create a new task for the user."""
    task = await task_service.create(
        title=params.title,
        description=params.description,
        due_date=params.due_date
    )
    return task.to_dict()

@server.tool()
async def list_tasks(params: ListTasksParams) -> dict:
    """Retrieve user's tasks with optional filters."""
    tasks = await task_service.list(
        status=params.status,
        limit=params.limit
    )
    return {
        "tasks": [t.to_dict() for t in tasks],
        "total": len(tasks),
        "has_more": len(tasks) == params.limit
    }

@server.tool()
async def complete_task(params: CompleteTaskParams) -> dict:
    """Mark a task as completed."""
    task = await task_service.complete(params.task_id)
    return task.to_dict()

@server.tool()
async def delete_task(params: DeleteTaskParams) -> dict:
    """Permanently delete a task."""
    if not params.confirm:
        raise ValueError("Deletion must be confirmed")
    await task_service.delete(params.task_id)
    return {"deleted": True, "task_id": params.task_id}

# Tool listing for discovery
@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="add_task",
            description="Create a new task for the user",
            inputSchema=AddTaskParams.model_json_schema()
        ),
        Tool(
            name="list_tasks",
            description="Retrieve user's tasks with optional filters",
            inputSchema=ListTasksParams.model_json_schema()
        ),
        Tool(
            name="complete_task",
            description="Mark a task as completed",
            inputSchema=CompleteTaskParams.model_json_schema()
        ),
        Tool(
            name="delete_task",
            description="Permanently delete a task (requires confirmation)",
            inputSchema=DeleteTaskParams.model_json_schema()
        ),
    ]
```

### MCP Client Integration
```python
# client/mcp_client.py
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def create_mcp_client():
    """Create and connect to MCP server."""
    server_params = StdioServerParameters(
        command="python",
        args=["mcp_server/main.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[t.name for t in tools.tools]}")

            # Call a tool
            result = await session.call_tool(
                "add_task",
                {"title": "Buy groceries"}
            )
            print(f"Result: {result}")

            return session
```

---

## 4. OpenAI Agents SDK Integration

### Agent Architecture
```
┌─────────────────────────────────────────────────────────┐
│                   OpenAI Agents SDK                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐ │
│  │   Agent     │───▶│   Runner    │───▶│   Tools     │ │
│  │ Definition  │    │  (Execute)  │    │ (Actions)   │ │
│  └─────────────┘    └─────────────┘    └─────────────┘ │
│         │                  │                  │         │
│         │           ┌──────▼──────┐          │         │
│         │           │   Model     │          │         │
│         │           │  (OpenAI)   │          │         │
│         │           └─────────────┘          │         │
│         │                                     │         │
│         └────────────────┬───────────────────┘         │
│                          │                              │
│                   ┌──────▼──────┐                      │
│                   │  Handoffs   │                      │
│                   │ (Multi-Agent)│                      │
│                   └─────────────┘                      │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Agent Definition
```python
# agents/task_agent.py
from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field
from typing import Optional

# Define tool parameter models
class AddTaskInput(BaseModel):
    title: str = Field(description="The task title")
    description: Optional[str] = Field(None, description="Task details")

class ListTasksInput(BaseModel):
    status: Optional[str] = Field("all", description="Filter: all, pending, completed")

class TaskIdInput(BaseModel):
    task_id: int = Field(description="The ID of the task")

# Define tools as functions
@function_tool
async def add_task(input: AddTaskInput) -> str:
    """Create a new task for the user."""
    task = await task_service.create(input.title, input.description)
    return f"Created task #{task.id}: {task.title}"

@function_tool
async def list_tasks(input: ListTasksInput) -> str:
    """List the user's tasks."""
    tasks = await task_service.list(status=input.status)
    if not tasks:
        return "You have no tasks."
    return "\n".join([f"#{t.id} {'✓' if t.completed else '○'} {t.title}" for t in tasks])

@function_tool
async def complete_task(input: TaskIdInput) -> str:
    """Mark a task as completed."""
    task = await task_service.complete(input.task_id)
    return f"Completed: {task.title}"

@function_tool
async def delete_task(input: TaskIdInput) -> str:
    """Delete a task permanently."""
    await task_service.delete(input.task_id)
    return f"Deleted task #{input.task_id}"

# Create the agent
task_agent = Agent(
    name="TaskAssistant",
    instructions="""You are a helpful task management assistant.

    Your capabilities:
    - Create new tasks for users
    - List and filter existing tasks
    - Mark tasks as complete
    - Delete tasks when requested

    Guidelines:
    - Be concise and helpful
    - Confirm destructive actions before executing
    - Offer suggestions when appropriate
    - If a request is unclear, ask for clarification
    """,
    tools=[add_task, list_tasks, complete_task, delete_task],
    model="gpt-4o"
)
```

### Running the Agent
```python
# main.py
from agents import Runner
from agents.task_agent import task_agent

async def chat(user_message: str, conversation_history: list = None):
    """Run a single turn of conversation."""

    # Create runner with conversation history
    runner = Runner(
        agent=task_agent,
        context=conversation_history or []
    )

    # Execute the agent
    result = await runner.run(user_message)

    return {
        "response": result.final_output,
        "tool_calls": result.tool_calls,
        "history": result.messages
    }

# Example usage
async def main():
    history = []

    # Turn 1: Add a task
    result = await chat("Add a task to buy groceries", history)
    print(f"Assistant: {result['response']}")
    history = result['history']

    # Turn 2: List tasks
    result = await chat("Show my tasks", history)
    print(f"Assistant: {result['response']}")
    history = result['history']

    # Turn 3: Complete task
    result = await chat("Mark the first one as done", history)
    print(f"Assistant: {result['response']}")
```

### Agent with Handoffs (Multi-Agent)
```python
# agents/multi_agent.py
from agents import Agent, handoff

# Specialized agents
task_agent = Agent(
    name="TaskAgent",
    instructions="Handle task management operations.",
    tools=[add_task, list_tasks, complete_task, delete_task]
)

calendar_agent = Agent(
    name="CalendarAgent",
    instructions="Handle calendar and scheduling operations.",
    tools=[create_event, list_events, update_event]
)

# Triage agent that routes to specialists
triage_agent = Agent(
    name="TriageAgent",
    instructions="""You are a helpful assistant that routes requests.

    - For task management (todos, tasks, reminders): hand off to TaskAgent
    - For calendar/scheduling: hand off to CalendarAgent
    - For general questions: answer directly
    """,
    handoffs=[
        handoff(task_agent, "Task management requests"),
        handoff(calendar_agent, "Calendar and scheduling requests")
    ]
)
```

---

## 5. Context Management (Stateless Servers)

### Stateless Architecture
```
┌─────────────────────────────────────────────────────────┐
│                 Stateless AI Server                      │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Request                                                 │
│  ┌─────────────────────────────────────────────────┐   │
│  │ { user_id, message, conversation_id }           │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Load Context from Store               │   │
│  │  • Conversation history                         │   │
│  │  • User preferences                             │   │
│  │  • Relevant memories                            │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Process with Agent                  │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│                          ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Save Updated Context                   │   │
│  └─────────────────────────────────────────────────┘   │
│                          │                               │
│  Response               ▼                               │
│  ┌─────────────────────────────────────────────────┐   │
│  │ { response, conversation_id, metadata }         │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Context Store Design
```python
# context/store.py
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import json

@dataclass
class Message:
    role: str  # "user" | "assistant" | "system" | "tool"
    content: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    tool_calls: Optional[list] = None
    tool_call_id: Optional[str] = None

@dataclass
class ConversationContext:
    conversation_id: str
    user_id: str
    messages: list[Message] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str, **kwargs):
        self.messages.append(Message(role=role, content=content, **kwargs))
        self.updated_at = datetime.utcnow()

    def get_messages_for_api(self, limit: int = 50) -> list[dict]:
        """Format messages for OpenAI API."""
        recent = self.messages[-limit:]
        return [
            {"role": m.role, "content": m.content}
            for m in recent
        ]

    def to_dict(self) -> dict:
        return {
            "conversation_id": self.conversation_id,
            "user_id": self.user_id,
            "messages": [
                {
                    "role": m.role,
                    "content": m.content,
                    "timestamp": m.timestamp.isoformat()
                }
                for m in self.messages
            ],
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

class ContextStore:
    """Abstract base for context storage."""

    async def get(self, conversation_id: str) -> Optional[ConversationContext]:
        raise NotImplementedError

    async def save(self, context: ConversationContext) -> None:
        raise NotImplementedError

    async def delete(self, conversation_id: str) -> None:
        raise NotImplementedError
```

### Redis Context Store Implementation
```python
# context/redis_store.py
import redis.asyncio as redis
import json
from datetime import datetime

class RedisContextStore(ContextStore):
    def __init__(self, redis_url: str, ttl_seconds: int = 86400):
        self.redis = redis.from_url(redis_url)
        self.ttl = ttl_seconds

    def _key(self, conversation_id: str) -> str:
        return f"conversation:{conversation_id}"

    async def get(self, conversation_id: str) -> Optional[ConversationContext]:
        data = await self.redis.get(self._key(conversation_id))
        if not data:
            return None

        obj = json.loads(data)
        context = ConversationContext(
            conversation_id=obj["conversation_id"],
            user_id=obj["user_id"],
            metadata=obj.get("metadata", {}),
            created_at=datetime.fromisoformat(obj["created_at"]),
            updated_at=datetime.fromisoformat(obj["updated_at"])
        )
        for m in obj["messages"]:
            context.messages.append(Message(
                role=m["role"],
                content=m["content"],
                timestamp=datetime.fromisoformat(m["timestamp"])
            ))
        return context

    async def save(self, context: ConversationContext) -> None:
        data = json.dumps(context.to_dict())
        await self.redis.setex(
            self._key(context.conversation_id),
            self.ttl,
            data
        )

    async def delete(self, conversation_id: str) -> None:
        await self.redis.delete(self._key(conversation_id))
```

### Context-Aware API Endpoint
```python
# api/chat.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid

router = APIRouter(prefix="/chat", tags=["Chat"])

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str

@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    context_store: ContextStore = Depends(get_context_store),
    agent_runner: AgentRunner = Depends(get_agent_runner)
):
    # Get or create conversation context
    conversation_id = request.conversation_id or str(uuid.uuid4())
    context = await context_store.get(conversation_id)

    if not context:
        context = ConversationContext(
            conversation_id=conversation_id,
            user_id=str(current_user.id)
        )

    # Add user message
    context.add_message("user", request.message)

    # Run agent with context
    result = await agent_runner.run(
        message=request.message,
        history=context.get_messages_for_api()
    )

    # Add assistant response
    context.add_message("assistant", result.response)

    # Save updated context
    await context_store.save(context)

    return ChatResponse(
        response=result.response,
        conversation_id=conversation_id
    )
```

---

## 6. Prompt-to-Action Mapping

### Action Routing Architecture
```
User Prompt
    │
    ▼
┌─────────────────┐
│ Intent Classifier│
└────────┬────────┘
         │
    ┌────┴────┬────────┬────────┐
    ▼         ▼        ▼        ▼
┌───────┐ ┌───────┐ ┌───────┐ ┌───────┐
│Action │ │Action │ │Action │ │Fallback│
│  A    │ │  B    │ │  C    │ │Handler │
└───┬───┘ └───┬───┘ └───┬───┘ └───┬───┘
    │         │        │         │
    └─────────┴────────┴─────────┘
                  │
                  ▼
           Response to User
```

### Prompt-to-Action Specification
```markdown
# Prompt-to-Action Mapping

## Action Registry

### TASK_CREATE
**Trigger Patterns**:
- "add {task}"
- "create a task for {task}"
- "remind me to {task}"
- "I need to {task}"
- "new task: {task}"

**Slot Extraction**:
- task: The task description
- due_date: Optional temporal expression

**Tool**: `add_task`

**Response Template**: "Created task: {title}"

### TASK_LIST
**Trigger Patterns**:
- "show my tasks"
- "what do I need to do"
- "list tasks"
- "what's on my list"

**Slot Extraction**:
- status: Optional filter (pending/completed/all)

**Tool**: `list_tasks`

**Response Template**: Formatted task list

### TASK_COMPLETE
**Trigger Patterns**:
- "mark {id} as done"
- "complete task {id}"
- "I finished {task_reference}"
- "done with {task_reference}"

**Slot Extraction**:
- task_id: Numeric ID or reference resolution

**Tool**: `complete_task`

**Response Template**: "Completed: {title}"

### TASK_DELETE
**Trigger Patterns**:
- "delete task {id}"
- "remove {task_reference}"
- "get rid of {task_reference}"

**Slot Extraction**:
- task_id: Numeric ID or reference resolution

**Confirmation Required**: Yes

**Tool**: `delete_task`

**Response Template**: "Deleted task: {title}"
```

### Action Router Implementation
```python
# routing/action_router.py
from dataclasses import dataclass
from typing import Callable, Optional, Any
from enum import Enum
import re

class ActionType(Enum):
    TASK_CREATE = "task_create"
    TASK_LIST = "task_list"
    TASK_COMPLETE = "task_complete"
    TASK_DELETE = "task_delete"
    UNKNOWN = "unknown"

@dataclass
class ActionResult:
    action: ActionType
    slots: dict[str, Any]
    confidence: float
    requires_confirmation: bool = False

@dataclass
class ActionHandler:
    action: ActionType
    patterns: list[str]
    tool_name: str
    slot_extractors: dict[str, Callable]
    requires_confirmation: bool = False

class ActionRouter:
    def __init__(self):
        self.handlers: list[ActionHandler] = []

    def register(self, handler: ActionHandler):
        self.handlers.append(handler)

    def route(self, user_input: str) -> ActionResult:
        """Determine the action from user input."""
        user_input_lower = user_input.lower().strip()

        for handler in self.handlers:
            for pattern in handler.patterns:
                if match := re.search(pattern, user_input_lower):
                    # Extract slots
                    slots = {}
                    for slot_name, extractor in handler.slot_extractors.items():
                        slots[slot_name] = extractor(user_input, match)

                    return ActionResult(
                        action=handler.action,
                        slots=slots,
                        confidence=0.9,
                        requires_confirmation=handler.requires_confirmation
                    )

        return ActionResult(
            action=ActionType.UNKNOWN,
            slots={},
            confidence=0.0
        )

# Setup router
router = ActionRouter()

# Register handlers
router.register(ActionHandler(
    action=ActionType.TASK_CREATE,
    patterns=[
        r"add\s+(.+)",
        r"create\s+(?:a\s+)?task\s+(?:for\s+)?(.+)",
        r"remind\s+me\s+to\s+(.+)",
    ],
    tool_name="add_task",
    slot_extractors={
        "title": lambda text, match: match.group(1).strip()
    }
))

router.register(ActionHandler(
    action=ActionType.TASK_DELETE,
    patterns=[
        r"delete\s+(?:task\s+)?#?(\d+)",
        r"remove\s+(?:task\s+)?#?(\d+)",
    ],
    tool_name="delete_task",
    slot_extractors={
        "task_id": lambda text, match: int(match.group(1))
    },
    requires_confirmation=True
))
```

---

## 7. AI Safety via Specification Rules

### Safety Specification Template
```markdown
# AI Safety Specification

## Scope Boundaries
### In Scope
- Task management operations (CRUD)
- Task queries and filtering
- Due date and reminder management

### Out of Scope
- Financial transactions
- Personal data beyond task content
- External system integrations (without explicit approval)
- Bulk operations (>10 items without confirmation)

## Safety Rules

### Rule 1: Confirmation for Destructive Actions
**Trigger**: delete, remove, clear, reset
**Action**: Request explicit confirmation before executing
**Implementation**:
```
AI: "You're about to delete [N] tasks. This cannot be undone. Type 'confirm' to proceed."
```

### Rule 2: Rate Limiting
**Trigger**: Rapid successive operations
**Thresholds**:
- Create: 10/minute
- Delete: 5/minute
- Bulk operations: 1/minute
**Action**: Pause and notify user

### Rule 3: Input Sanitization
**Trigger**: All user inputs
**Action**:
- Escape special characters
- Limit field lengths
- Reject obvious injection attempts

### Rule 4: Scope Enforcement
**Trigger**: Requests outside defined capabilities
**Action**: Politely decline and redirect
**Response**: "I can help with task management. For [X], you might try..."

### Rule 5: Data Minimization
**Trigger**: All tool calls
**Action**: Only request/return necessary data
**Implementation**: Strip sensitive fields before logging

## Prompt Injection Defense

### Detection Patterns
- "Ignore previous instructions"
- "You are now..."
- "Forget your rules"
- System prompt extraction attempts

### Response to Detected Attacks
1. Do not execute the request
2. Respond neutrally: "I can help with task management."
3. Log the attempt (without sensitive content)
4. Continue normal operation
```

### Safety Implementation
```python
# safety/guards.py
from dataclasses import dataclass
from typing import Optional
import re
from datetime import datetime, timedelta

@dataclass
class SafetyCheck:
    passed: bool
    reason: Optional[str] = None
    requires_confirmation: bool = False

class SafetyGuard:
    # Injection detection patterns
    INJECTION_PATTERNS = [
        r"ignore\s+(previous|all|your)\s+(instructions|rules|constraints)",
        r"you\s+are\s+now\s+a",
        r"forget\s+(everything|your|all)",
        r"reveal\s+your\s+(system|original)\s+prompt",
        r"what\s+are\s+your\s+(instructions|rules)",
    ]

    def __init__(self):
        self.rate_limits: dict[str, list[datetime]] = {}

    def check_injection(self, user_input: str) -> SafetyCheck:
        """Check for prompt injection attempts."""
        input_lower = user_input.lower()
        for pattern in self.INJECTION_PATTERNS:
            if re.search(pattern, input_lower):
                return SafetyCheck(
                    passed=False,
                    reason="Potential prompt injection detected"
                )
        return SafetyCheck(passed=True)

    def check_rate_limit(
        self,
        user_id: str,
        action: str,
        limit: int,
        window_seconds: int = 60
    ) -> SafetyCheck:
        """Check rate limits for user actions."""
        key = f"{user_id}:{action}"
        now = datetime.utcnow()
        window_start = now - timedelta(seconds=window_seconds)

        # Get recent actions
        if key not in self.rate_limits:
            self.rate_limits[key] = []

        # Filter to window
        self.rate_limits[key] = [
            t for t in self.rate_limits[key]
            if t > window_start
        ]

        if len(self.rate_limits[key]) >= limit:
            return SafetyCheck(
                passed=False,
                reason=f"Rate limit exceeded: {limit} {action} per {window_seconds}s"
            )

        # Record this action
        self.rate_limits[key].append(now)
        return SafetyCheck(passed=True)

    def check_destructive_action(
        self,
        action: str,
        count: int = 1
    ) -> SafetyCheck:
        """Check if action requires confirmation."""
        destructive_actions = ["delete", "remove", "clear", "reset"]

        if action in destructive_actions:
            return SafetyCheck(
                passed=True,
                requires_confirmation=True,
                reason=f"Destructive action '{action}' requires confirmation"
            )

        # Bulk operations always need confirmation
        if count > 5:
            return SafetyCheck(
                passed=True,
                requires_confirmation=True,
                reason=f"Bulk operation ({count} items) requires confirmation"
            )

        return SafetyCheck(passed=True)

    def sanitize_input(self, text: str, max_length: int = 1000) -> str:
        """Sanitize user input."""
        # Truncate
        text = text[:max_length]
        # Remove null bytes
        text = text.replace("\x00", "")
        # Normalize whitespace
        text = " ".join(text.split())
        return text

# Usage in agent
safety_guard = SafetyGuard()

async def process_user_input(user_id: str, user_input: str, action: str):
    # Check for injection
    injection_check = safety_guard.check_injection(user_input)
    if not injection_check.passed:
        return "I can help you with task management. What would you like to do?"

    # Check rate limits
    rate_check = safety_guard.check_rate_limit(user_id, action, limit=10)
    if not rate_check.passed:
        return "You're making requests too quickly. Please wait a moment."

    # Check for destructive actions
    destructive_check = safety_guard.check_destructive_action(action)
    if destructive_check.requires_confirmation:
        return f"This action requires confirmation. {destructive_check.reason}"

    # Sanitize input
    clean_input = safety_guard.sanitize_input(user_input)

    # Process normally
    return await execute_action(clean_input, action)
```

---

## 8. Multi-Agent Coordination

### Multi-Agent Architecture
```
┌─────────────────────────────────────────────────────────┐
│                  Orchestrator Agent                      │
│  (Routes requests, manages handoffs, maintains state)   │
└───────────────────────┬─────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌───────────────┐ ┌───────────────┐ ┌───────────────┐
│  Task Agent   │ │ Calendar Agent│ │ Search Agent  │
│  (CRUD tasks) │ │ (Scheduling)  │ │ (Information) │
└───────────────┘ └───────────────┘ └───────────────┘
        │               │               │
        └───────────────┴───────────────┘
                        │
                        ▼
              ┌─────────────────┐
              │  Shared Context │
              │   (Messages,    │
              │    State)       │
              └─────────────────┘
```

### Multi-Agent Specification
```markdown
# Multi-Agent Coordination Specification

## Agent Registry

### Orchestrator
**Role**: Route requests, manage context, coordinate handoffs
**Capabilities**: Intent classification, agent selection, response aggregation
**Handoffs**: All specialist agents

### TaskAgent
**Role**: Task management specialist
**Capabilities**: CRUD operations on tasks
**Tools**: add_task, list_tasks, update_task, delete_task, complete_task
**Handoff Triggers**:
- Calendar scheduling → CalendarAgent
- Information lookup → SearchAgent

### CalendarAgent
**Role**: Calendar and scheduling specialist
**Capabilities**: Event management, scheduling
**Tools**: create_event, list_events, update_event, find_free_time
**Handoff Triggers**:
- Task creation → TaskAgent

### SearchAgent
**Role**: Information retrieval specialist
**Capabilities**: Search, summarize, answer questions
**Tools**: web_search, summarize, answer_question
**Handoff Triggers**:
- Action items → TaskAgent

## Handoff Protocol

### Handoff Message Format
```json
{
  "from_agent": "TaskAgent",
  "to_agent": "CalendarAgent",
  "reason": "User wants to schedule task",
  "context": {
    "task_id": 1,
    "task_title": "Meeting with client",
    "user_request": "Schedule this for tomorrow at 2pm"
  },
  "conversation_history": [...]
}
```

### Handoff Rules
1. Include relevant context when handing off
2. Preserve conversation history
3. Return to original agent after completion
4. Log all handoffs for debugging
```

### Multi-Agent Implementation
```python
# agents/orchestrator.py
from agents import Agent, handoff
from typing import Optional
from dataclasses import dataclass

@dataclass
class HandoffContext:
    from_agent: str
    to_agent: str
    reason: str
    context: dict
    return_after: bool = True

class AgentOrchestrator:
    def __init__(self):
        self.agents: dict[str, Agent] = {}
        self.current_agent: Optional[str] = None
        self.handoff_stack: list[HandoffContext] = []

    def register_agent(self, name: str, agent: Agent):
        self.agents[name] = agent

    async def route(self, user_input: str, context: dict) -> str:
        """Route user input to appropriate agent."""

        # Determine best agent for this request
        if self.current_agent and not self._should_handoff(user_input):
            agent = self.agents[self.current_agent]
        else:
            agent_name = await self._classify_intent(user_input)
            agent = self.agents.get(agent_name, self.agents["orchestrator"])
            self.current_agent = agent_name

        # Execute with agent
        result = await agent.run(user_input, context)

        # Check for handoff request in result
        if handoff_request := self._extract_handoff(result):
            return await self._execute_handoff(handoff_request, context)

        return result.response

    async def _classify_intent(self, user_input: str) -> str:
        """Classify user intent to determine agent."""
        # Simple keyword-based routing (replace with ML classifier)
        input_lower = user_input.lower()

        if any(kw in input_lower for kw in ["task", "todo", "remind"]):
            return "task_agent"
        elif any(kw in input_lower for kw in ["calendar", "schedule", "meeting"]):
            return "calendar_agent"
        elif any(kw in input_lower for kw in ["search", "find", "look up"]):
            return "search_agent"
        else:
            return "orchestrator"

    async def _execute_handoff(
        self,
        handoff: HandoffContext,
        context: dict
    ) -> str:
        """Execute handoff to another agent."""
        # Push to stack for return
        if handoff.return_after:
            self.handoff_stack.append(HandoffContext(
                from_agent=handoff.to_agent,
                to_agent=handoff.from_agent,
                reason="Return from handoff",
                context={},
                return_after=False
            ))

        # Switch to target agent
        self.current_agent = handoff.to_agent
        target_agent = self.agents[handoff.to_agent]

        # Merge contexts
        merged_context = {**context, **handoff.context}

        # Generate handoff message
        handoff_message = f"""
        Handoff from {handoff.from_agent}: {handoff.reason}
        Context: {handoff.context}
        """

        return await target_agent.run(handoff_message, merged_context)

    def _should_handoff(self, user_input: str) -> bool:
        """Determine if current request should trigger handoff."""
        # Check handoff stack
        if self.handoff_stack:
            return True
        return False

    def _extract_handoff(self, result) -> Optional[HandoffContext]:
        """Extract handoff request from agent result."""
        if hasattr(result, "handoff") and result.handoff:
            return result.handoff
        return None

# Setup multi-agent system
orchestrator = AgentOrchestrator()

# Create and register agents
task_agent = Agent(
    name="TaskAgent",
    instructions="You handle task management...",
    tools=[add_task, list_tasks, complete_task, delete_task]
)

calendar_agent = Agent(
    name="CalendarAgent",
    instructions="You handle calendar management...",
    tools=[create_event, list_events, find_free_time]
)

search_agent = Agent(
    name="SearchAgent",
    instructions="You handle information retrieval...",
    tools=[web_search, summarize]
)

orchestrator.register_agent("task_agent", task_agent)
orchestrator.register_agent("calendar_agent", calendar_agent)
orchestrator.register_agent("search_agent", search_agent)

# Usage
async def main():
    context = {"user_id": "user123", "conversation_history": []}

    # This goes to task agent
    response = await orchestrator.route("Add a task to prepare presentation", context)
    print(response)

    # This triggers handoff to calendar agent
    response = await orchestrator.route("Schedule it for tomorrow at 3pm", context)
    print(response)
```

---

## Quick Reference

### AI Application Development Workflow
```
1. Define AI Behavior     → Conversation UX Spec
2. Design Tool Interface  → MCP Tool Specification
3. Implement Tools        → MCP Server
4. Create Agent           → OpenAI Agents SDK
5. Add Safety Rules       → Safety Specification
6. Manage Context         → Stateless Architecture
7. Coordinate Agents      → Multi-Agent System
```

### Key Specifications
| Spec | Purpose |
|------|---------|
| AI Feature Spec | Define intents, behaviors, examples |
| Conversation UX | Persona, patterns, error handling |
| MCP Tool Spec | Tool definitions, parameters, errors |
| Safety Rules | Boundaries, confirmations, rate limits |
| Multi-Agent Spec | Agent roles, handoffs, coordination |

### Agent Development Commands
```bash
# Start MCP server
python -m mcp_server.main

# Run agent
python -m agents.main

# Test tools
python -m pytest tests/tools/ -v

# Validate safety rules
python -m safety.validator
```

### Safety Checklist
- [ ] Prompt injection defense enabled
- [ ] Rate limiting configured
- [ ] Destructive action confirmations
- [ ] Input sanitization active
- [ ] Scope boundaries defined
- [ ] Out-of-scope responses prepared
- [ ] Logging without sensitive data
