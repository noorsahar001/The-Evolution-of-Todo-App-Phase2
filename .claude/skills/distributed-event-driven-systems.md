# Skill: Distributed & Event-Driven Systems Engineering

A comprehensive skill for building production-grade distributed systems with event-driven architectures, message streaming, and cloud-native deployment using Spec-Driven Development.

---

## 1. Distributed Systems Architecture

### Overview
Distributed systems are collections of independent computers that appear to users as a single coherent system. They provide scalability, fault tolerance, and geographic distribution.

### CAP Theorem
```
┌─────────────────────────────────────────────────────────┐
│                    CAP Theorem                           │
├─────────────────────────────────────────────────────────┤
│                                                          │
│              Consistency (C)                             │
│                   /\                                     │
│                  /  \                                    │
│                 /    \                                   │
│                / CA   \                                  │
│               /        \                                 │
│              /──────────\                               │
│             /            \                               │
│            /   CP    AP   \                              │
│           /                \                             │
│          ──────────────────                             │
│    Availability (A)      Partition                       │
│                          Tolerance (P)                   │
│                                                          │
│  Pick 2 (in practice, P is required, choose C or A)    │
│                                                          │
│  CP: Strong consistency, may reject writes              │
│  AP: High availability, eventual consistency            │
│  CA: Not realistic in distributed systems               │
└─────────────────────────────────────────────────────────┘
```

### Distributed Architecture Patterns
```
┌─────────────────────────────────────────────────────────┐
│            Distributed System Patterns                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Leader-Follower                                     │
│     ┌────────┐                                          │
│     │ Leader │──writes──▶ Followers (read replicas)    │
│     └────────┘                                          │
│                                                          │
│  2. Peer-to-Peer                                        │
│     ┌────┐   ┌────┐   ┌────┐                           │
│     │Node│◀─▶│Node│◀─▶│Node│                           │
│     └────┘   └────┘   └────┘                           │
│                                                          │
│  3. Event Sourcing                                      │
│     Events ──▶ Event Store ──▶ Projections             │
│                                                          │
│  4. CQRS (Command Query Responsibility Segregation)    │
│     Commands ──▶ Write Model                            │
│     Queries  ──▶ Read Model                             │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Distributed Architecture Specification
```markdown
# Distributed Architecture Specification

## System Overview
- **Name**: [System Name]
- **Type**: Microservices / Event-Driven / Hybrid
- **Consistency Model**: Strong / Eventual / Causal

## Services

### Service: [Service Name]
- **Responsibility**: [Single responsibility]
- **Scaling**: Horizontal (stateless) / Vertical (stateful)
- **Replicas**: Min 2, Max 10
- **State**: Stateless / Stateful (describe state)

### Communication Matrix
| From | To | Protocol | Pattern | Timeout |
|------|-----|----------|---------|---------|
| API Gateway | Task Service | gRPC | Sync | 5s |
| Task Service | Notification | Kafka | Async | - |
| Task Service | User Service | HTTP | Sync | 3s |

## Data Consistency

### Consistency Requirements
| Operation | Consistency | Rationale |
|-----------|-------------|-----------|
| Create Task | Strong | User expects immediate confirmation |
| List Tasks | Eventual | Read replicas acceptable |
| Update Task | Strong | Conflict resolution needed |

### Conflict Resolution
- **Strategy**: Last-Write-Wins / Merge / Manual
- **Vector Clocks**: [If applicable]
- **CRDTs**: [If applicable]

## Failure Handling

### Failure Modes
| Failure | Detection | Recovery | Fallback |
|---------|-----------|----------|----------|
| Service down | Health check | Restart pod | Circuit breaker |
| Network partition | Timeout | Retry with backoff | Cached response |
| Data corruption | Checksum | Restore from backup | Read replica |

### Circuit Breaker Config
- **Failure Threshold**: 5 failures
- **Reset Timeout**: 30 seconds
- **Half-Open Requests**: 3

## Idempotency

### Idempotent Operations
| Operation | Idempotency Key | Storage | TTL |
|-----------|-----------------|---------|-----|
| Create Task | Request-ID header | Redis | 24h |
| Process Payment | Transaction-ID | PostgreSQL | 7d |
```

### Consensus and Coordination
```python
# patterns/distributed_lock.py
"""Distributed lock implementation using Redis."""

import redis
import uuid
import time
from contextlib import contextmanager
from typing import Optional

class DistributedLock:
    """Redis-based distributed lock with automatic renewal."""

    def __init__(
        self,
        redis_client: redis.Redis,
        lock_name: str,
        ttl_seconds: int = 30,
        retry_delay: float = 0.1,
        retry_count: int = 100
    ):
        self.redis = redis_client
        self.lock_name = f"lock:{lock_name}"
        self.ttl = ttl_seconds
        self.retry_delay = retry_delay
        self.retry_count = retry_count
        self.lock_id: Optional[str] = None

    def acquire(self) -> bool:
        """Attempt to acquire the lock."""
        self.lock_id = str(uuid.uuid4())

        for _ in range(self.retry_count):
            # SET NX with expiration (atomic operation)
            acquired = self.redis.set(
                self.lock_name,
                self.lock_id,
                nx=True,  # Only set if not exists
                ex=self.ttl  # Expiration in seconds
            )

            if acquired:
                return True

            time.sleep(self.retry_delay)

        return False

    def release(self) -> bool:
        """Release the lock if we own it."""
        if not self.lock_id:
            return False

        # Lua script for atomic check-and-delete
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """

        result = self.redis.eval(lua_script, 1, self.lock_name, self.lock_id)
        self.lock_id = None
        return result == 1

    def extend(self, additional_seconds: int) -> bool:
        """Extend the lock TTL if we own it."""
        if not self.lock_id:
            return False

        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("expire", KEYS[1], ARGV[2])
        else
            return 0
        end
        """

        result = self.redis.eval(
            lua_script, 1,
            self.lock_name, self.lock_id, additional_seconds
        )
        return result == 1

    @contextmanager
    def __call__(self):
        """Context manager for lock acquisition."""
        if not self.acquire():
            raise LockAcquisitionError(f"Could not acquire lock: {self.lock_name}")
        try:
            yield self
        finally:
            self.release()

class LockAcquisitionError(Exception):
    pass

# Usage
redis_client = redis.Redis(host='localhost', port=6379)

def process_payment(payment_id: str):
    lock = DistributedLock(redis_client, f"payment:{payment_id}")

    with lock():
        # Critical section - only one process can execute
        payment = get_payment(payment_id)
        if payment.status == "pending":
            execute_payment(payment)
            payment.status = "completed"
            save_payment(payment)
```

---

## 2. Event-Driven Design (Kafka)

### Event-Driven Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│              Event-Driven Architecture                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Producers              Kafka               Consumers    │
│  ┌─────────┐     ┌─────────────────┐     ┌─────────┐   │
│  │ Service │────▶│  Topic: tasks   │────▶│ Service │   │
│  │    A    │     │  ┌───┬───┬───┐  │     │    C    │   │
│  └─────────┘     │  │P0 │P1 │P2 │  │     └─────────┘   │
│                  │  └───┴───┴───┘  │                    │
│  ┌─────────┐     │                 │     ┌─────────┐   │
│  │ Service │────▶│  Topic: users   │────▶│ Service │   │
│  │    B    │     │  ┌───┬───┐      │     │    D    │   │
│  └─────────┘     │  │P0 │P1 │      │     └─────────┘   │
│                  │  └───┴───┘      │                    │
│                  └─────────────────┘                    │
│                                                          │
│  Key Concepts:                                          │
│  • Topics: Named channels for events                    │
│  • Partitions: Parallel units within topics             │
│  • Consumer Groups: Scalable consumption                │
│  • Offset: Position in partition                        │
└─────────────────────────────────────────────────────────┘
```

### Kafka Topic Specification
```markdown
# Kafka Topic Specification

## Topic: task-events

### Overview
- **Purpose**: Task lifecycle events (created, updated, completed, deleted)
- **Retention**: 7 days
- **Partitions**: 6 (based on expected throughput)
- **Replication Factor**: 3

### Event Schema (Avro)
```json
{
  "type": "record",
  "name": "TaskEvent",
  "namespace": "com.example.tasks",
  "fields": [
    {"name": "event_id", "type": "string"},
    {"name": "event_type", "type": {"type": "enum", "name": "EventType",
      "symbols": ["CREATED", "UPDATED", "COMPLETED", "DELETED"]}},
    {"name": "task_id", "type": "string"},
    {"name": "user_id", "type": "string"},
    {"name": "timestamp", "type": "long", "logicalType": "timestamp-millis"},
    {"name": "payload", "type": ["null", "string"], "default": null},
    {"name": "metadata", "type": {"type": "map", "values": "string"}}
  ]
}
```

### Partitioning Strategy
- **Key**: user_id (ensures user's events are ordered)
- **Rationale**: User operations must be processed in order

### Consumer Groups
| Group ID | Purpose | Instances |
|----------|---------|-----------|
| task-processor | Process task operations | 3 |
| task-notifier | Send notifications | 2 |
| task-analytics | Analytics aggregation | 1 |

### SLAs
- **Throughput**: 10,000 events/second
- **Latency**: p99 < 100ms (produce), p99 < 500ms (consume)
- **Durability**: No data loss (acks=all)
```

### Kafka Producer Implementation
```python
# messaging/kafka_producer.py
"""Kafka producer with reliability guarantees."""

from confluent_kafka import Producer, KafkaError
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroSerializer
from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Optional, Callable
import json
import uuid

@dataclass
class TaskEvent:
    event_type: str
    task_id: str
    user_id: str
    payload: Optional[dict] = None
    event_id: str = None
    timestamp: int = None

    def __post_init__(self):
        if self.event_id is None:
            self.event_id = str(uuid.uuid4())
        if self.timestamp is None:
            self.timestamp = int(datetime.utcnow().timestamp() * 1000)

class KafkaEventProducer:
    """Production-grade Kafka producer."""

    def __init__(
        self,
        bootstrap_servers: str,
        schema_registry_url: str,
        topic: str
    ):
        # Producer configuration for reliability
        self.producer = Producer({
            'bootstrap.servers': bootstrap_servers,
            'acks': 'all',  # Wait for all replicas
            'retries': 10,
            'retry.backoff.ms': 100,
            'enable.idempotence': True,  # Exactly-once semantics
            'max.in.flight.requests.per.connection': 5,
            'compression.type': 'snappy',
            'linger.ms': 5,  # Batch for efficiency
            'batch.size': 16384,
        })

        self.topic = topic

        # Schema registry for Avro serialization
        schema_registry = SchemaRegistryClient({'url': schema_registry_url})
        self.serializer = AvroSerializer(
            schema_registry,
            self._get_schema(),
            self._to_dict
        )

    def _get_schema(self) -> str:
        return json.dumps({
            "type": "record",
            "name": "TaskEvent",
            "fields": [
                {"name": "event_id", "type": "string"},
                {"name": "event_type", "type": "string"},
                {"name": "task_id", "type": "string"},
                {"name": "user_id", "type": "string"},
                {"name": "timestamp", "type": "long"},
                {"name": "payload", "type": ["null", "string"], "default": None},
            ]
        })

    def _to_dict(self, event: TaskEvent, ctx) -> dict:
        return {
            "event_id": event.event_id,
            "event_type": event.event_type,
            "task_id": event.task_id,
            "user_id": event.user_id,
            "timestamp": event.timestamp,
            "payload": json.dumps(event.payload) if event.payload else None,
        }

    def _delivery_callback(self, err, msg):
        """Callback for delivery confirmation."""
        if err:
            print(f"Delivery failed: {err}")
            # In production: send to dead letter queue, alert
        else:
            print(f"Delivered to {msg.topic()}[{msg.partition()}]@{msg.offset()}")

    def publish(
        self,
        event: TaskEvent,
        callback: Callable = None
    ):
        """Publish event to Kafka."""
        try:
            self.producer.produce(
                topic=self.topic,
                key=event.user_id.encode('utf-8'),  # Partition by user
                value=self.serializer(event, None),
                callback=callback or self._delivery_callback,
                headers={
                    'event_type': event.event_type,
                    'correlation_id': event.event_id,
                }
            )
            # Trigger delivery callbacks
            self.producer.poll(0)

        except BufferError:
            # Queue is full, wait and retry
            self.producer.poll(1)
            self.publish(event, callback)

    def flush(self, timeout: float = 10.0):
        """Wait for all messages to be delivered."""
        remaining = self.producer.flush(timeout)
        if remaining > 0:
            raise RuntimeError(f"{remaining} messages still pending")

# Usage
producer = KafkaEventProducer(
    bootstrap_servers="kafka:9092",
    schema_registry_url="http://schema-registry:8081",
    topic="task-events"
)

# Publish task created event
event = TaskEvent(
    event_type="CREATED",
    task_id="task-123",
    user_id="user-456",
    payload={"title": "Buy groceries", "priority": "high"}
)
producer.publish(event)
producer.flush()
```

### Kafka Consumer Implementation
```python
# messaging/kafka_consumer.py
"""Kafka consumer with at-least-once processing."""

from confluent_kafka import Consumer, KafkaError, KafkaException
from confluent_kafka.schema_registry import SchemaRegistryClient
from confluent_kafka.schema_registry.avro import AvroDeserializer
from dataclasses import dataclass
from typing import Callable, List
import json
import signal

class KafkaEventConsumer:
    """Production-grade Kafka consumer with graceful shutdown."""

    def __init__(
        self,
        bootstrap_servers: str,
        schema_registry_url: str,
        group_id: str,
        topics: List[str],
        auto_commit: bool = False
    ):
        self.consumer = Consumer({
            'bootstrap.servers': bootstrap_servers,
            'group.id': group_id,
            'auto.offset.reset': 'earliest',
            'enable.auto.commit': auto_commit,
            'max.poll.interval.ms': 300000,  # 5 minutes for processing
            'session.timeout.ms': 45000,
            'heartbeat.interval.ms': 15000,
        })

        self.topics = topics
        self.running = True

        # Schema registry for Avro deserialization
        schema_registry = SchemaRegistryClient({'url': schema_registry_url})
        self.deserializer = AvroDeserializer(
            schema_registry,
            self._get_schema()
        )

        # Graceful shutdown
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)

    def _get_schema(self) -> str:
        return json.dumps({
            "type": "record",
            "name": "TaskEvent",
            "fields": [
                {"name": "event_id", "type": "string"},
                {"name": "event_type", "type": "string"},
                {"name": "task_id", "type": "string"},
                {"name": "user_id", "type": "string"},
                {"name": "timestamp", "type": "long"},
                {"name": "payload", "type": ["null", "string"], "default": None},
            ]
        })

    def _shutdown(self, signum, frame):
        """Handle shutdown signal."""
        print("Shutdown signal received")
        self.running = False

    def consume(self, handler: Callable[[dict], bool]):
        """
        Consume messages and process with handler.

        Handler should return True for successful processing,
        False to indicate failure (won't commit offset).
        """
        self.consumer.subscribe(self.topics)
        print(f"Subscribed to topics: {self.topics}")

        try:
            while self.running:
                msg = self.consumer.poll(1.0)

                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition, not an error
                        continue
                    else:
                        raise KafkaException(msg.error())

                # Deserialize message
                try:
                    event = self.deserializer(
                        msg.value(),
                        None  # SerializationContext
                    )

                    # Parse payload if present
                    if event.get('payload'):
                        event['payload'] = json.loads(event['payload'])

                    # Process message
                    if handler(event):
                        # Commit offset on success
                        self.consumer.commit(asynchronous=False)
                    else:
                        # Processing failed, don't commit
                        # Message will be redelivered
                        print(f"Processing failed for event: {event['event_id']}")

                except Exception as e:
                    print(f"Error processing message: {e}")
                    # Don't commit, will retry

        finally:
            # Clean shutdown
            self.consumer.close()
            print("Consumer closed")

# Usage
def handle_task_event(event: dict) -> bool:
    """Process task event."""
    print(f"Processing event: {event['event_type']} for task {event['task_id']}")

    try:
        if event['event_type'] == 'CREATED':
            # Send notification
            send_notification(event['user_id'], f"Task created: {event['payload']['title']}")
        elif event['event_type'] == 'COMPLETED':
            # Update analytics
            update_completion_stats(event['user_id'])

        return True  # Success

    except Exception as e:
        print(f"Handler error: {e}")
        return False  # Will retry

consumer = KafkaEventConsumer(
    bootstrap_servers="kafka:9092",
    schema_registry_url="http://schema-registry:8081",
    group_id="task-notifier",
    topics=["task-events"]
)

consumer.consume(handle_task_event)
```

---

## 3. Async Processing & Messaging

### Message Queue Patterns
```
┌─────────────────────────────────────────────────────────┐
│              Messaging Patterns                          │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  1. Point-to-Point (Queue)                              │
│     Producer ──▶ Queue ──▶ Consumer                     │
│                  (one consumer gets each message)       │
│                                                          │
│  2. Publish-Subscribe (Topic)                           │
│     Producer ──▶ Topic ──▶ Consumer A                   │
│                      └──▶ Consumer B                    │
│                      └──▶ Consumer C                    │
│                  (all consumers get all messages)       │
│                                                          │
│  3. Request-Reply                                       │
│     Requester ──▶ Request Queue ──▶ Responder          │
│     Requester ◀── Reply Queue ◀──── Responder          │
│                                                          │
│  4. Dead Letter Queue                                   │
│     Queue ──failed──▶ DLQ ──▶ Manual Review            │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Async Processing Specification
```markdown
# Async Processing Specification

## Background Jobs

### Job: send-notification
- **Trigger**: task.created, task.completed events
- **Priority**: High
- **Timeout**: 30 seconds
- **Retries**: 3 (exponential backoff)
- **Dead Letter**: After 3 failures

### Job: generate-report
- **Trigger**: Scheduled (daily at 00:00 UTC)
- **Priority**: Low
- **Timeout**: 10 minutes
- **Retries**: 2
- **Concurrency**: 1 (singleton)

### Job: sync-external
- **Trigger**: On-demand via API
- **Priority**: Medium
- **Timeout**: 5 minutes
- **Retries**: 5
- **Rate Limit**: 10/minute

## Queue Configuration

### High Priority Queue
- **Name**: jobs:high
- **Workers**: 5
- **Prefetch**: 1
- **Visibility Timeout**: 60s

### Default Queue
- **Name**: jobs:default
- **Workers**: 10
- **Prefetch**: 5
- **Visibility Timeout**: 300s

### Low Priority Queue
- **Name**: jobs:low
- **Workers**: 2
- **Prefetch**: 10
- **Visibility Timeout**: 600s

## Error Handling

### Retry Strategy
| Attempt | Delay |
|---------|-------|
| 1 | 1 second |
| 2 | 5 seconds |
| 3 | 30 seconds |
| 4 | 2 minutes |
| 5 | 10 minutes |

### Dead Letter Processing
- Review daily
- Auto-retry after 24 hours (once)
- Alert if DLQ depth > 100
```

### Task Queue Implementation (Redis + RQ)
```python
# workers/task_queue.py
"""Background job processing with Redis Queue."""

from redis import Redis
from rq import Queue, Worker, Retry
from rq.job import Job
from dataclasses import dataclass
from datetime import timedelta
from typing import Callable, Any, Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Queue configuration
redis_conn = Redis(host='localhost', port=6379, db=0)

queues = {
    'high': Queue('high', connection=redis_conn),
    'default': Queue('default', connection=redis_conn),
    'low': Queue('low', connection=redis_conn),
}

@dataclass
class JobConfig:
    """Job configuration."""
    timeout: int = 300  # 5 minutes
    retries: int = 3
    retry_delays: list = None
    result_ttl: int = 86400  # 24 hours
    failure_ttl: int = 604800  # 7 days

    def __post_init__(self):
        if self.retry_delays is None:
            self.retry_delays = [1, 5, 30, 120, 600]  # Exponential backoff

def enqueue_job(
    func: Callable,
    *args,
    queue: str = 'default',
    config: JobConfig = None,
    job_id: str = None,
    **kwargs
) -> Job:
    """Enqueue a job with configuration."""
    config = config or JobConfig()
    q = queues.get(queue, queues['default'])

    # Build retry configuration
    retry = Retry(
        max=config.retries,
        interval=config.retry_delays[:config.retries]
    )

    job = q.enqueue(
        func,
        *args,
        **kwargs,
        job_id=job_id,
        job_timeout=config.timeout,
        result_ttl=config.result_ttl,
        failure_ttl=config.failure_ttl,
        retry=retry,
    )

    logger.info(f"Enqueued job {job.id} to {queue} queue")
    return job

# Job definitions
def send_notification(user_id: str, message: str, channel: str = 'email'):
    """Send notification to user."""
    logger.info(f"Sending {channel} notification to {user_id}: {message}")
    # Implementation here
    return {"status": "sent", "user_id": user_id}

def generate_daily_report(date: str):
    """Generate daily analytics report."""
    logger.info(f"Generating report for {date}")
    # Long-running task
    return {"status": "completed", "date": date}

def sync_external_service(service: str, batch_size: int = 100):
    """Sync data with external service."""
    logger.info(f"Syncing {batch_size} records with {service}")
    # Implementation here
    return {"status": "synced", "count": batch_size}

# Usage examples
if __name__ == "__main__":
    # High priority notification
    job1 = enqueue_job(
        send_notification,
        user_id="user-123",
        message="Your task is complete!",
        queue='high',
        config=JobConfig(timeout=30, retries=3)
    )

    # Low priority report
    job2 = enqueue_job(
        generate_daily_report,
        date="2024-01-15",
        queue='low',
        config=JobConfig(timeout=600, retries=2)
    )

    print(f"Job 1 ID: {job1.id}")
    print(f"Job 2 ID: {job2.id}")
```

### Worker Process
```python
# workers/run_worker.py
"""Worker process for background jobs."""

from redis import Redis
from rq import Worker, Queue, Connection
import sys

redis_conn = Redis(host='localhost', port=6379, db=0)

# Queue priority order
queue_names = ['high', 'default', 'low']

def run_worker():
    """Run worker with all queues."""
    with Connection(redis_conn):
        queues = [Queue(name) for name in queue_names]

        worker = Worker(
            queues,
            name=f'worker-{sys.argv[1] if len(sys.argv) > 1 else "1"}',
        )

        worker.work(
            with_scheduler=True,
            logging_level='INFO',
        )

if __name__ == '__main__':
    run_worker()
```

### Saga Pattern for Distributed Transactions
```python
# patterns/saga.py
"""Saga pattern for distributed transactions."""

from dataclasses import dataclass, field
from typing import Callable, List, Optional, Any
from enum import Enum
import logging

logger = logging.getLogger(__name__)

class SagaStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    COMPENSATING = "compensating"
    COMPENSATED = "compensated"
    FAILED = "failed"

@dataclass
class SagaStep:
    """Single step in a saga."""
    name: str
    action: Callable[..., Any]
    compensation: Callable[..., Any]
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    result: Any = None
    error: Optional[Exception] = None

@dataclass
class Saga:
    """
    Saga orchestrator for distributed transactions.

    Executes steps in order. If any step fails,
    compensates all completed steps in reverse order.
    """
    name: str
    steps: List[SagaStep] = field(default_factory=list)
    status: SagaStatus = SagaStatus.PENDING
    completed_steps: List[SagaStep] = field(default_factory=list)

    def add_step(
        self,
        name: str,
        action: Callable,
        compensation: Callable,
        *args,
        **kwargs
    ):
        """Add a step to the saga."""
        step = SagaStep(
            name=name,
            action=action,
            compensation=compensation,
            args=args,
            kwargs=kwargs
        )
        self.steps.append(step)
        return self

    def execute(self) -> bool:
        """Execute the saga."""
        self.status = SagaStatus.RUNNING
        logger.info(f"Starting saga: {self.name}")

        for step in self.steps:
            try:
                logger.info(f"Executing step: {step.name}")
                step.result = step.action(*step.args, **step.kwargs)
                self.completed_steps.append(step)
                logger.info(f"Step completed: {step.name}")

            except Exception as e:
                logger.error(f"Step failed: {step.name} - {e}")
                step.error = e
                self._compensate()
                return False

        self.status = SagaStatus.COMPLETED
        logger.info(f"Saga completed: {self.name}")
        return True

    def _compensate(self):
        """Compensate all completed steps in reverse order."""
        self.status = SagaStatus.COMPENSATING
        logger.info(f"Starting compensation for saga: {self.name}")

        # Reverse order compensation
        for step in reversed(self.completed_steps):
            try:
                logger.info(f"Compensating step: {step.name}")
                step.compensation(*step.args, **step.kwargs)
                logger.info(f"Compensation completed: {step.name}")

            except Exception as e:
                logger.error(f"Compensation failed: {step.name} - {e}")
                # In production: alert, manual intervention needed
                self.status = SagaStatus.FAILED
                return

        self.status = SagaStatus.COMPENSATED
        logger.info(f"Saga compensated: {self.name}")

# Example: Order processing saga
def reserve_inventory(order_id: str, items: list):
    print(f"Reserving inventory for order {order_id}")
    return {"reservation_id": "res-123"}

def release_inventory(order_id: str, items: list):
    print(f"Releasing inventory for order {order_id}")

def charge_payment(order_id: str, amount: float):
    print(f"Charging ${amount} for order {order_id}")
    # Simulate failure
    # raise Exception("Payment failed")
    return {"transaction_id": "txn-456"}

def refund_payment(order_id: str, amount: float):
    print(f"Refunding ${amount} for order {order_id}")

def create_shipment(order_id: str, address: str):
    print(f"Creating shipment for order {order_id}")
    return {"shipment_id": "ship-789"}

def cancel_shipment(order_id: str, address: str):
    print(f"Cancelling shipment for order {order_id}")

# Build and execute saga
saga = Saga(name="process-order")
saga.add_step(
    "reserve_inventory",
    reserve_inventory,
    release_inventory,
    order_id="order-123",
    items=["item-1", "item-2"]
)
saga.add_step(
    "charge_payment",
    charge_payment,
    refund_payment,
    order_id="order-123",
    amount=99.99
)
saga.add_step(
    "create_shipment",
    create_shipment,
    cancel_shipment,
    order_id="order-123",
    address="123 Main St"
)

success = saga.execute()
print(f"Saga success: {success}, Status: {saga.status}")
```

---

## 4. Dapr Runtime Concepts

### Dapr Architecture Overview
```
┌─────────────────────────────────────────────────────────┐
│                    Dapr Architecture                     │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Your Application                                        │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Application Code                    │   │
│  └───────────────────┬─────────────────────────────┘   │
│                      │ HTTP/gRPC                        │
│                      ▼                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │              Dapr Sidecar                        │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  Building Blocks:                               │   │
│  │  • Service Invocation                           │   │
│  │  • State Management                             │   │
│  │  • Pub/Sub Messaging                            │   │
│  │  • Bindings (Input/Output)                      │   │
│  │  • Actors                                        │   │
│  │  • Secrets Management                           │   │
│  │  • Configuration                                │   │
│  │  • Distributed Lock                             │   │
│  └───────────────────┬─────────────────────────────┘   │
│                      │                                  │
│                      ▼                                  │
│  ┌─────────────────────────────────────────────────┐   │
│  │           Component Configuration               │   │
│  │  (Redis, Kafka, PostgreSQL, Azure, AWS...)     │   │
│  └─────────────────────────────────────────────────┘   │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

### Dapr Component Specifications
```yaml
# dapr/components/statestore.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app
spec:
  type: state.redis
  version: v1
  metadata:
    - name: redisHost
      value: "redis:6379"
    - name: redisPassword
      secretKeyRef:
        name: redis-secret
        key: password
    - name: actorStateStore
      value: "true"
    - name: keyPrefix
      value: "name"  # Use app-id as key prefix
  scopes:
    - api
    - worker

---
# dapr/components/pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka:9092"
    - name: consumerGroup
      value: "todo-app"
    - name: authRequired
      value: "false"
    - name: maxMessageBytes
      value: "1048576"  # 1MB
  scopes:
    - api
    - worker
    - notifier

---
# dapr/components/bindings-cron.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: scheduled-tasks
  namespace: todo-app
spec:
  type: bindings.cron
  version: v1
  metadata:
    - name: schedule
      value: "0 0 * * *"  # Daily at midnight
  scopes:
    - worker

---
# dapr/components/secrets.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secrets
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
  metadata: []
```

### Dapr Subscription Configuration
```yaml
# dapr/subscriptions/task-events.yaml
apiVersion: dapr.io/v2alpha1
kind: Subscription
metadata:
  name: task-events-subscription
  namespace: todo-app
spec:
  pubsubname: pubsub
  topic: task-events
  routes:
    default: /events/tasks
    rules:
      - match: event.type == "task.created"
        path: /events/tasks/created
      - match: event.type == "task.completed"
        path: /events/tasks/completed
  scopes:
    - notifier
  deadLetterTopic: task-events-dlq
  bulkSubscribe:
    enabled: true
    maxMessagesCount: 100
    maxAwaitDurationMs: 1000
```

### Dapr Application Integration
```python
# app/dapr_client.py
"""Dapr integration for application services."""

from dapr.clients import DaprClient
from dapr.clients.grpc._state import StateItem, StateOptions, Consistency, Concurrency
from dataclasses import dataclass, asdict
from typing import Optional, List, Any
import json

@dataclass
class Task:
    id: str
    title: str
    completed: bool = False
    user_id: str = ""

class DaprTaskService:
    """Task service using Dapr building blocks."""

    def __init__(self, state_store: str = "statestore", pubsub: str = "pubsub"):
        self.state_store = state_store
        self.pubsub = pubsub

    async def create_task(self, task: Task) -> Task:
        """Create task using Dapr state store and publish event."""
        with DaprClient() as client:
            # Save to state store
            client.save_state(
                store_name=self.state_store,
                key=f"task:{task.id}",
                value=json.dumps(asdict(task)),
                state_metadata={
                    "contentType": "application/json"
                },
                options=StateOptions(
                    consistency=Consistency.strong,
                    concurrency=Concurrency.first_write
                )
            )

            # Publish event
            client.publish_event(
                pubsub_name=self.pubsub,
                topic_name="task-events",
                data=json.dumps({
                    "type": "task.created",
                    "task_id": task.id,
                    "user_id": task.user_id,
                    "payload": asdict(task)
                }),
                data_content_type="application/json",
                publish_metadata={
                    "cloudevent.type": "task.created",
                    "cloudevent.source": "task-service"
                }
            )

            return task

    async def get_task(self, task_id: str) -> Optional[Task]:
        """Get task from Dapr state store."""
        with DaprClient() as client:
            state = client.get_state(
                store_name=self.state_store,
                key=f"task:{task_id}"
            )

            if state.data:
                data = json.loads(state.data)
                return Task(**data)
            return None

    async def list_tasks(self, user_id: str) -> List[Task]:
        """Query tasks for a user."""
        with DaprClient() as client:
            # Using state query (requires supported store like MongoDB, CosmosDB)
            query = {
                "filter": {
                    "EQ": {"user_id": user_id}
                },
                "sort": [{"key": "created_at", "order": "DESC"}],
                "page": {"limit": 100}
            }

            response = client.query_state(
                store_name=self.state_store,
                query=json.dumps(query)
            )

            tasks = []
            for item in response.results:
                data = json.loads(item.value)
                tasks.append(Task(**data))

            return tasks

    async def complete_task(self, task_id: str) -> Optional[Task]:
        """Mark task as completed with optimistic concurrency."""
        with DaprClient() as client:
            # Get current state with ETag
            state = client.get_state(
                store_name=self.state_store,
                key=f"task:{task_id}"
            )

            if not state.data:
                return None

            task_data = json.loads(state.data)
            task_data["completed"] = True

            # Save with ETag for optimistic concurrency
            client.save_state(
                store_name=self.state_store,
                key=f"task:{task_id}",
                value=json.dumps(task_data),
                etag=state.etag,
                options=StateOptions(
                    concurrency=Concurrency.first_write
                )
            )

            # Publish completion event
            client.publish_event(
                pubsub_name=self.pubsub,
                topic_name="task-events",
                data=json.dumps({
                    "type": "task.completed",
                    "task_id": task_id,
                    "user_id": task_data["user_id"]
                }),
                data_content_type="application/json"
            )

            return Task(**task_data)

    async def invoke_service(self, app_id: str, method: str, data: Any) -> Any:
        """Invoke another service via Dapr service invocation."""
        with DaprClient() as client:
            response = client.invoke_method(
                app_id=app_id,
                method_name=method,
                data=json.dumps(data),
                content_type="application/json"
            )

            return json.loads(response.data)
```

### Dapr FastAPI Integration
```python
# app/main.py
"""FastAPI application with Dapr integration."""

from fastapi import FastAPI, HTTPException
from cloudevents.http import from_http
from dapr.ext.fastapi import DaprApp
from pydantic import BaseModel
from typing import Optional

app = FastAPI()
dapr_app = DaprApp(app)

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TaskResponse(BaseModel):
    id: str
    title: str
    completed: bool

# Dapr pub/sub subscription endpoint
@dapr_app.subscribe(pubsub="pubsub", topic="task-events", route="/events/tasks")
async def handle_task_event(event: dict):
    """Handle task events from pub/sub."""
    print(f"Received event: {event}")

    event_type = event.get("type")
    task_id = event.get("task_id")

    if event_type == "task.created":
        # Send notification
        print(f"Task {task_id} was created")
    elif event_type == "task.completed":
        # Update analytics
        print(f"Task {task_id} was completed")

    return {"status": "SUCCESS"}

# Dapr input binding for scheduled tasks
@app.post("/scheduled-tasks")
async def handle_scheduled_binding():
    """Handle scheduled job from Dapr binding."""
    print("Running scheduled task...")
    # Perform scheduled work
    return {"status": "completed"}

# Health endpoints for Dapr
@app.get("/health/live")
async def health_live():
    return {"status": "healthy"}

@app.get("/health/ready")
async def health_ready():
    return {"status": "ready"}
```

---

## 5. Microservices Communication

### Communication Patterns Specification
```markdown
# Microservices Communication Specification

## Synchronous Communication

### REST API
- **Use Case**: User-facing requests, CRUD operations
- **Protocol**: HTTP/1.1 or HTTP/2
- **Format**: JSON
- **Timeout**: 30 seconds (gateway), 5 seconds (internal)

### gRPC
- **Use Case**: Internal service-to-service, high throughput
- **Protocol**: HTTP/2
- **Format**: Protocol Buffers
- **Timeout**: 5 seconds default

## Asynchronous Communication

### Event-Driven (Kafka)
- **Use Case**: Event sourcing, audit logs, cross-service notifications
- **Delivery**: At-least-once
- **Ordering**: Per partition (partition by user_id/entity_id)

### Command Queue (Redis)
- **Use Case**: Background jobs, deferred processing
- **Delivery**: At-least-once with acknowledgment
- **Priority**: High, Default, Low queues

## Communication Matrix

| From | To | Pattern | Protocol | Timeout | Retry |
|------|-----|---------|----------|---------|-------|
| Gateway | Task API | Sync | REST | 30s | 3x |
| Task API | User API | Sync | gRPC | 5s | 2x |
| Task API | Notification | Async | Kafka | - | - |
| Task API | Analytics | Async | Kafka | - | - |
| Scheduler | Worker | Async | Redis | - | 5x |

## Resilience Patterns

### Circuit Breaker
- **Failure Threshold**: 5 errors in 10s
- **Open Duration**: 30s
- **Half-Open Requests**: 3

### Retry Policy
- **Max Retries**: 3
- **Backoff**: Exponential (1s, 2s, 4s)
- **Jitter**: +/- 20%

### Bulkhead
- **Concurrent Requests**: 100 per service
- **Queue Size**: 50
- **Timeout**: 5s
```

### gRPC Service Definition
```protobuf
// proto/task_service.proto
syntax = "proto3";

package tasks.v1;

option go_package = "github.com/example/tasks/v1;tasksv1";

import "google/protobuf/timestamp.proto";
import "google/protobuf/empty.proto";

service TaskService {
  // Create a new task
  rpc CreateTask(CreateTaskRequest) returns (Task);

  // Get task by ID
  rpc GetTask(GetTaskRequest) returns (Task);

  // List tasks for a user
  rpc ListTasks(ListTasksRequest) returns (ListTasksResponse);

  // Update task
  rpc UpdateTask(UpdateTaskRequest) returns (Task);

  // Delete task
  rpc DeleteTask(DeleteTaskRequest) returns (google.protobuf.Empty);

  // Stream task updates (server streaming)
  rpc WatchTasks(WatchTasksRequest) returns (stream TaskEvent);
}

message Task {
  string id = 1;
  string user_id = 2;
  string title = 3;
  string description = 4;
  bool completed = 5;
  google.protobuf.Timestamp created_at = 6;
  google.protobuf.Timestamp updated_at = 7;
}

message CreateTaskRequest {
  string user_id = 1;
  string title = 2;
  string description = 3;
}

message GetTaskRequest {
  string id = 1;
}

message ListTasksRequest {
  string user_id = 1;
  TaskFilter filter = 2;
  int32 page_size = 3;
  string page_token = 4;
}

message TaskFilter {
  optional bool completed = 1;
}

message ListTasksResponse {
  repeated Task tasks = 1;
  string next_page_token = 2;
  int32 total_count = 3;
}

message UpdateTaskRequest {
  string id = 1;
  optional string title = 2;
  optional string description = 3;
  optional bool completed = 4;
}

message DeleteTaskRequest {
  string id = 1;
}

message WatchTasksRequest {
  string user_id = 1;
}

message TaskEvent {
  string event_type = 1;  // CREATED, UPDATED, DELETED
  Task task = 2;
  google.protobuf.Timestamp timestamp = 3;
}
```

### Service Mesh with Resilience
```python
# communication/resilience.py
"""Resilience patterns for microservices communication."""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Callable, TypeVar, Generic, Optional
from enum import Enum
import random
import functools

T = TypeVar('T')

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

@dataclass
class CircuitBreakerConfig:
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: float = 30.0
    half_open_max_calls: int = 3

@dataclass
class CircuitBreaker:
    """Circuit breaker pattern implementation."""
    name: str
    config: CircuitBreakerConfig = field(default_factory=CircuitBreakerConfig)
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0
    half_open_calls: int = 0

    def _should_allow_request(self) -> bool:
        if self.state == CircuitState.CLOSED:
            return True

        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.config.timeout:
                self.state = CircuitState.HALF_OPEN
                self.half_open_calls = 0
                return True
            return False

        # HALF_OPEN
        return self.half_open_calls < self.config.half_open_max_calls

    def _record_success(self):
        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.config.success_threshold:
                self.state = CircuitState.CLOSED
                self.failure_count = 0
                self.success_count = 0

    def _record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()

        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.OPEN
            self.failure_count = 0
        elif self.failure_count >= self.config.failure_threshold:
            self.state = CircuitState.OPEN

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        if not self._should_allow_request():
            raise CircuitOpenError(f"Circuit {self.name} is open")

        if self.state == CircuitState.HALF_OPEN:
            self.half_open_calls += 1

        try:
            result = await func(*args, **kwargs)
            self._record_success()
            return result
        except Exception as e:
            self._record_failure()
            raise

class CircuitOpenError(Exception):
    pass

@dataclass
class RetryConfig:
    max_retries: int = 3
    base_delay: float = 1.0
    max_delay: float = 30.0
    exponential_base: float = 2.0
    jitter: float = 0.2

async def retry_with_backoff(
    func: Callable[..., T],
    config: RetryConfig = None,
    *args,
    **kwargs
) -> T:
    """Retry with exponential backoff and jitter."""
    config = config or RetryConfig()

    last_exception = None

    for attempt in range(config.max_retries + 1):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            last_exception = e

            if attempt == config.max_retries:
                break

            # Calculate delay with exponential backoff
            delay = min(
                config.base_delay * (config.exponential_base ** attempt),
                config.max_delay
            )

            # Add jitter
            jitter = delay * config.jitter * (2 * random.random() - 1)
            delay += jitter

            print(f"Attempt {attempt + 1} failed, retrying in {delay:.2f}s")
            await asyncio.sleep(delay)

    raise last_exception

@dataclass
class BulkheadConfig:
    max_concurrent: int = 100
    max_queue: int = 50
    timeout: float = 5.0

class Bulkhead:
    """Bulkhead pattern to limit concurrent requests."""

    def __init__(self, name: str, config: BulkheadConfig = None):
        self.name = name
        self.config = config or BulkheadConfig()
        self.semaphore = asyncio.Semaphore(self.config.max_concurrent)
        self.queue_size = 0

    async def call(self, func: Callable[..., T], *args, **kwargs) -> T:
        if self.queue_size >= self.config.max_queue:
            raise BulkheadFullError(f"Bulkhead {self.name} queue is full")

        self.queue_size += 1
        try:
            async with asyncio.timeout(self.config.timeout):
                async with self.semaphore:
                    return await func(*args, **kwargs)
        finally:
            self.queue_size -= 1

class BulkheadFullError(Exception):
    pass

# Combined resilience decorator
def resilient(
    circuit_breaker: CircuitBreaker = None,
    retry_config: RetryConfig = None,
    bulkhead: Bulkhead = None
):
    """Decorator combining resilience patterns."""
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async def call():
                return await func(*args, **kwargs)

            # Apply patterns in order: bulkhead -> circuit breaker -> retry
            operation = call

            if circuit_breaker:
                original = operation
                operation = lambda: circuit_breaker.call(original)

            if retry_config:
                original = operation
                operation = lambda: retry_with_backoff(original, retry_config)

            if bulkhead:
                original = operation
                operation = lambda: bulkhead.call(original)

            return await operation()

        return wrapper
    return decorator

# Usage example
task_service_breaker = CircuitBreaker("task-service")
task_service_bulkhead = Bulkhead("task-service", BulkheadConfig(max_concurrent=50))

@resilient(
    circuit_breaker=task_service_breaker,
    retry_config=RetryConfig(max_retries=3),
    bulkhead=task_service_bulkhead
)
async def call_task_service(task_id: str):
    """Call task service with full resilience."""
    # HTTP call to task service
    pass
```

---

## 6. CI/CD Pipeline Design via Specs

### CI/CD Pipeline Specification
```markdown
# CI/CD Pipeline Specification

## Pipeline Overview

### Stages
1. **Build**: Compile, lint, test
2. **Security**: SAST, dependency scan, secrets detection
3. **Package**: Container build, push to registry
4. **Deploy Dev**: Auto-deploy to development
5. **Integration Test**: Run E2E tests
6. **Deploy Staging**: Deploy to staging
7. **Approval**: Manual gate
8. **Deploy Production**: Blue-green deployment

## Triggers

| Event | Action |
|-------|--------|
| Push to feature/* | Build + Test |
| PR to main | Build + Test + Security |
| Merge to main | Full pipeline to staging |
| Tag v*.*.* | Full pipeline to production |

## Quality Gates

### Build Stage
- [ ] All tests pass
- [ ] Code coverage > 80%
- [ ] Lint errors = 0
- [ ] Type check passes

### Security Stage
- [ ] No critical/high vulnerabilities
- [ ] No secrets in code
- [ ] SAST findings addressed
- [ ] License compliance

### Integration Stage
- [ ] API contract tests pass
- [ ] E2E tests pass
- [ ] Performance baseline met

## Deployment Strategy

### Development
- **Strategy**: Rolling update
- **Replicas**: 1
- **Approval**: None

### Staging
- **Strategy**: Rolling update
- **Replicas**: 2
- **Approval**: Auto (after tests)

### Production
- **Strategy**: Blue-Green
- **Replicas**: 3+
- **Approval**: Manual
- **Rollback**: Automatic on failure
```

### GitHub Actions Pipeline
```yaml
# .github/workflows/ci-cd.yaml
name: CI/CD Pipeline

on:
  push:
    branches: [main, 'feature/**']
    tags: ['v*.*.*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # Stage 1: Build and Test
  build:
    name: Build and Test
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}

    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Determine version
        id: version
        run: |
          if [[ "${{ github.ref }}" == refs/tags/* ]]; then
            echo "version=${GITHUB_REF#refs/tags/}" >> $GITHUB_OUTPUT
          else
            echo "version=sha-${GITHUB_SHA::8}" >> $GITHUB_OUTPUT
          fi

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
          cache: 'pip'

      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt

      - name: Lint
        run: |
          ruff check .
          mypy app/

      - name: Test
        run: |
          pytest tests/ -v --cov=app --cov-report=xml --cov-fail-under=80

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: coverage.xml

  # Stage 2: Security Scanning
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: build

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

      - name: Dependency Review
        if: github.event_name == 'pull_request'
        uses: actions/dependency-review-action@v3

  # Stage 3: Build and Push Container
  package:
    name: Build Container
    runs-on: ubuntu-latest
    needs: [build, security]
    if: github.event_name != 'pull_request'

    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.version }}
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Scan container image
        uses: aquasecurity/trivy-action@master
        with:
          image-ref: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ needs.build.outputs.version }}
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  # Stage 4: Deploy to Development
  deploy-dev:
    name: Deploy to Development
    runs-on: ubuntu-latest
    needs: [build, package]
    if: github.ref == 'refs/heads/main'
    environment: development

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Dev
        uses: ./.github/actions/deploy
        with:
          environment: dev
          version: ${{ needs.build.outputs.version }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_DEV }}

  # Stage 5: Integration Tests
  integration-test:
    name: Integration Tests
    runs-on: ubuntu-latest
    needs: deploy-dev
    environment: development

    steps:
      - uses: actions/checkout@v4

      - name: Run E2E Tests
        run: |
          npm install
          npm run test:e2e
        env:
          API_URL: ${{ vars.DEV_API_URL }}

      - name: Run Contract Tests
        run: |
          npm run test:contract

  # Stage 6: Deploy to Staging
  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: [build, integration-test]
    environment: staging

    steps:
      - uses: actions/checkout@v4

      - name: Deploy to Staging
        uses: ./.github/actions/deploy
        with:
          environment: staging
          version: ${{ needs.build.outputs.version }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_STAGING }}

  # Stage 7: Deploy to Production (manual approval)
  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: [build, deploy-staging]
    if: startsWith(github.ref, 'refs/tags/v')
    environment:
      name: production
      url: https://app.example.com

    steps:
      - uses: actions/checkout@v4

      - name: Blue-Green Deploy
        uses: ./.github/actions/blue-green-deploy
        with:
          version: ${{ needs.build.outputs.version }}
          kubeconfig: ${{ secrets.KUBE_CONFIG_PROD }}

      - name: Smoke Tests
        run: |
          ./scripts/smoke-test.sh https://app.example.com

      - name: Notify Success
        uses: slackapi/slack-github-action@v1
        with:
          payload: |
            {
              "text": "Deployed ${{ needs.build.outputs.version }} to production"
            }
        env:
          SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK }}
```

### Deployment Action
```yaml
# .github/actions/deploy/action.yaml
name: Deploy to Kubernetes
description: Deploy application to Kubernetes cluster

inputs:
  environment:
    description: Target environment
    required: true
  version:
    description: Version to deploy
    required: true
  kubeconfig:
    description: Kubernetes config
    required: true

runs:
  using: composite
  steps:
    - name: Set up kubectl
      uses: azure/setup-kubectl@v3

    - name: Configure kubeconfig
      shell: bash
      run: |
        echo "${{ inputs.kubeconfig }}" | base64 -d > kubeconfig
        export KUBECONFIG=kubeconfig

    - name: Deploy with Helm
      shell: bash
      run: |
        helm upgrade --install todo-app ./charts/todo-app \
          --namespace todo-app-${{ inputs.environment }} \
          --create-namespace \
          -f ./charts/todo-app/values-${{ inputs.environment }}.yaml \
          --set image.tag=${{ inputs.version }} \
          --wait --timeout 10m

    - name: Verify deployment
      shell: bash
      run: |
        kubectl rollout status deployment/todo-app-api \
          -n todo-app-${{ inputs.environment }} \
          --timeout=5m
```

---

## 7. Observability & Monitoring Concepts

### Observability Specification
```markdown
# Observability Specification

## Three Pillars

### Metrics
- **Tool**: Prometheus + Grafana
- **Retention**: 15 days (raw), 1 year (downsampled)
- **Scrape Interval**: 15s

### Logs
- **Tool**: Loki + Grafana
- **Retention**: 30 days
- **Format**: JSON structured

### Traces
- **Tool**: Jaeger / Tempo
- **Retention**: 7 days
- **Sampling**: 10% (production), 100% (errors)

## Key Metrics

### RED Method (Request-oriented)
- **Rate**: Requests per second
- **Errors**: Error rate percentage
- **Duration**: Request latency (p50, p95, p99)

### USE Method (Resource-oriented)
- **Utilization**: CPU, memory usage percentage
- **Saturation**: Queue depth, thread pool usage
- **Errors**: System errors, OOM events

## SLIs and SLOs

| Service | SLI | SLO | Alert Threshold |
|---------|-----|-----|-----------------|
| API | Availability | 99.9% | < 99.5% |
| API | Latency p99 | < 500ms | > 1000ms |
| API | Error rate | < 0.1% | > 1% |
| Worker | Job success rate | > 99% | < 95% |
| Worker | Job latency p95 | < 30s | > 60s |

## Alerting Rules

### Critical (Page)
- Service down > 1 minute
- Error rate > 5%
- Latency p99 > 5s

### Warning (Slack)
- Error rate > 1%
- Latency p95 > 1s
- CPU > 80% for 5m
- Memory > 85% for 5m
```

### Prometheus Metrics (Python)
```python
# observability/metrics.py
"""Prometheus metrics for application monitoring."""

from prometheus_client import Counter, Histogram, Gauge, Info
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import FastAPI, Request, Response
from functools import wraps
import time

# Application metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds',
    'HTTP request latency',
    ['method', 'endpoint'],
    buckets=[.005, .01, .025, .05, .1, .25, .5, 1, 2.5, 5, 10]
)

ACTIVE_REQUESTS = Gauge(
    'http_requests_active',
    'Active HTTP requests',
    ['method', 'endpoint']
)

# Business metrics
TASKS_CREATED = Counter(
    'tasks_created_total',
    'Total tasks created',
    ['user_type']
)

TASKS_COMPLETED = Counter(
    'tasks_completed_total',
    'Total tasks completed',
    ['user_type']
)

TASK_COMPLETION_TIME = Histogram(
    'task_completion_duration_seconds',
    'Time from creation to completion',
    buckets=[60, 300, 900, 3600, 86400, 604800]  # 1m to 1w
)

# System metrics
APP_INFO = Info('app', 'Application information')

def setup_metrics(app: FastAPI, version: str):
    """Setup metrics middleware and endpoint."""

    APP_INFO.info({
        'version': version,
        'python_version': '3.11',
    })

    @app.middleware("http")
    async def metrics_middleware(request: Request, call_next):
        method = request.method
        endpoint = request.url.path

        ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).inc()

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        ACTIVE_REQUESTS.labels(method=method, endpoint=endpoint).dec()
        REQUEST_COUNT.labels(
            method=method,
            endpoint=endpoint,
            status=response.status_code
        ).inc()
        REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

        return response

    @app.get("/metrics")
    async def metrics():
        return Response(
            generate_latest(),
            media_type=CONTENT_TYPE_LATEST
        )

# Business metric helpers
def record_task_created(user_type: str = "standard"):
    TASKS_CREATED.labels(user_type=user_type).inc()

def record_task_completed(user_type: str = "standard", duration_seconds: float = None):
    TASKS_COMPLETED.labels(user_type=user_type).inc()
    if duration_seconds:
        TASK_COMPLETION_TIME.observe(duration_seconds)
```

### Structured Logging
```python
# observability/logging.py
"""Structured logging with correlation."""

import logging
import json
import sys
from datetime import datetime
from contextvars import ContextVar
from typing import Optional
import uuid

# Context for request correlation
correlation_id: ContextVar[str] = ContextVar('correlation_id', default='')
user_id: ContextVar[str] = ContextVar('user_id', default='')

class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "correlation_id": correlation_id.get(),
            "user_id": user_id.get(),
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add extra fields
        if hasattr(record, 'extra'):
            log_data.update(record.extra)

        return json.dumps(log_data)

def setup_logging(level: str = "INFO"):
    """Configure structured logging."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())

    logging.basicConfig(
        level=getattr(logging, level),
        handlers=[handler]
    )

class LoggerAdapter(logging.LoggerAdapter):
    """Logger adapter with extra context."""

    def process(self, msg, kwargs):
        extra = kwargs.get('extra', {})
        extra['correlation_id'] = correlation_id.get()
        extra['user_id'] = user_id.get()
        kwargs['extra'] = extra
        return msg, kwargs

def get_logger(name: str) -> LoggerAdapter:
    """Get a logger with context."""
    return LoggerAdapter(logging.getLogger(name), {})

# FastAPI middleware for correlation ID
from fastapi import Request

async def correlation_middleware(request: Request, call_next):
    # Get or generate correlation ID
    corr_id = request.headers.get('X-Correlation-ID', str(uuid.uuid4()))
    correlation_id.set(corr_id)

    # Get user ID from auth token if present
    if hasattr(request.state, 'user'):
        user_id.set(request.state.user.id)

    response = await call_next(request)
    response.headers['X-Correlation-ID'] = corr_id

    return response

# Usage
logger = get_logger(__name__)
logger.info("Task created", extra={"task_id": "123", "title": "Buy groceries"})
```

### Distributed Tracing
```python
# observability/tracing.py
"""OpenTelemetry distributed tracing."""

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat
from opentelemetry.sdk.resources import Resource
from functools import wraps

def setup_tracing(
    service_name: str,
    otlp_endpoint: str = "http://tempo:4317",
    environment: str = "development"
):
    """Configure OpenTelemetry tracing."""

    # Resource attributes
    resource = Resource.create({
        "service.name": service_name,
        "service.version": "1.0.0",
        "deployment.environment": environment,
    })

    # Setup tracer provider
    provider = TracerProvider(resource=resource)

    # OTLP exporter
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    processor = BatchSpanProcessor(exporter)
    provider.add_span_processor(processor)

    trace.set_tracer_provider(provider)

    # Set propagator for distributed tracing
    set_global_textmap(B3MultiFormat())

    return trace.get_tracer(service_name)

def instrument_app(app, engine=None, redis_client=None):
    """Instrument FastAPI app and dependencies."""

    # FastAPI
    FastAPIInstrumentor.instrument_app(app)

    # HTTP client
    HTTPXClientInstrumentor().instrument()

    # SQLAlchemy
    if engine:
        SQLAlchemyInstrumentor().instrument(engine=engine)

    # Redis
    if redis_client:
        RedisInstrumentor().instrument()

# Custom span decorator
def traced(name: str = None, attributes: dict = None):
    """Decorator to trace a function."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            tracer = trace.get_tracer(__name__)
            span_name = name or func.__name__

            with tracer.start_as_current_span(span_name) as span:
                if attributes:
                    for key, value in attributes.items():
                        span.set_attribute(key, value)

                try:
                    result = await func(*args, **kwargs)
                    span.set_status(trace.Status(trace.StatusCode.OK))
                    return result
                except Exception as e:
                    span.set_status(trace.Status(trace.StatusCode.ERROR, str(e)))
                    span.record_exception(e)
                    raise

        return wrapper
    return decorator

# Usage
@traced(name="create_task", attributes={"operation": "create"})
async def create_task(task_data: dict):
    # This will be traced
    pass
```

---

## 8. Production-Grade Cloud Deployment

### Production Deployment Specification
```markdown
# Production Deployment Specification

## Infrastructure

### Cloud Provider: AWS/GCP/Azure
- **Region**: us-east-1 (primary), eu-west-1 (DR)
- **Kubernetes**: EKS/GKE/AKS (managed)
- **Version**: 1.28+

### Cluster Configuration
- **Control Plane**: Managed, multi-AZ
- **Node Groups**:
  - System: 3x t3.medium (cluster services)
  - Application: 3-10x t3.large (autoscaling)
  - Worker: 2-5x t3.xlarge (background jobs)

### Networking
- **VPC**: Dedicated, /16 CIDR
- **Subnets**: Public + Private per AZ
- **Load Balancer**: ALB/NLB
- **DNS**: Route53/Cloud DNS
- **CDN**: CloudFront/Cloud CDN

## High Availability

### Application Layer
- **Replicas**: Min 3 per service
- **Pod Disruption Budget**: minAvailable 2
- **Anti-Affinity**: Spread across AZs

### Data Layer
- **Database**: Multi-AZ RDS/Cloud SQL
- **Cache**: ElastiCache/Memorystore cluster
- **Message Queue**: MSK/Confluent Cloud

### Disaster Recovery
- **RPO**: 1 hour
- **RTO**: 4 hours
- **Backup**: Daily snapshots, 30-day retention
- **Cross-Region**: Async replication

## Security

### Network
- **WAF**: AWS WAF / Cloud Armor
- **DDoS**: Shield / Cloud Armor
- **Network Policies**: Calico/Cilium

### Access
- **RBAC**: Least privilege
- **IAM**: Service accounts with IRSA/Workload Identity
- **Secrets**: External Secrets + Vault/Secrets Manager

### Compliance
- **Encryption**: At-rest (KMS) + In-transit (TLS 1.3)
- **Audit**: CloudTrail / Audit Logs
- **Scanning**: Container + dependency scanning
```

### Production Helm Values
```yaml
# values-prod.yaml
global:
  imageRegistry: ghcr.io/myorg
  imagePullSecrets:
    - name: regcred

api:
  replicaCount: 3

  image:
    repository: api
    pullPolicy: Always

  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 2000m
      memory: 2Gi

  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilization: 70
    targetMemoryUtilization: 80
    behavior:
      scaleUp:
        stabilizationWindowSeconds: 60
      scaleDown:
        stabilizationWindowSeconds: 300

  affinity:
    podAntiAffinity:
      requiredDuringSchedulingIgnoredDuringExecution:
        - labelSelector:
            matchLabels:
              app.kubernetes.io/name: api
          topologyKey: topology.kubernetes.io/zone

  topologySpreadConstraints:
    - maxSkew: 1
      topologyKey: topology.kubernetes.io/zone
      whenUnsatisfiable: DoNotSchedule
      labelSelector:
        matchLabels:
          app.kubernetes.io/name: api

podDisruptionBudget:
  enabled: true
  minAvailable: 2

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
    nginx.ingress.kubernetes.io/proxy-connect-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-read-timeout: "30"
    nginx.ingress.kubernetes.io/proxy-send-timeout: "30"
  hosts:
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
          service: api
  tls:
    - secretName: api-tls
      hosts:
        - api.example.com

# External database (managed)
postgresql:
  enabled: false

externalDatabase:
  host: db.cluster-xxx.us-east-1.rds.amazonaws.com
  port: 5432
  database: todoapp
  existingSecret: db-credentials
  existingSecretPasswordKey: password

# External Redis (managed)
redis:
  enabled: false

externalRedis:
  host: redis.xxx.cache.amazonaws.com
  port: 6379
  existingSecret: redis-credentials

# External Kafka (managed)
kafka:
  enabled: false

externalKafka:
  brokers: b-1.kafka.xxx.kafka.us-east-1.amazonaws.com:9092
  existingSecret: kafka-credentials

# Monitoring
metrics:
  enabled: true
  serviceMonitor:
    enabled: true
    interval: 15s
    scrapeTimeout: 10s

# Network Policy
networkPolicy:
  enabled: true
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - port: 8000
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/name: prometheus
      ports:
        - port: 9090
```

### Production Checklist
```markdown
# Production Deployment Checklist

## Pre-Deployment
- [ ] All tests passing (unit, integration, E2E)
- [ ] Security scan passed (no critical/high vulnerabilities)
- [ ] Performance baseline validated
- [ ] Runbook updated
- [ ] Rollback plan documented

## Infrastructure
- [ ] Database migrated and verified
- [ ] Secrets rotated and verified
- [ ] SSL certificates valid (>30 days)
- [ ] DNS configured and propagated
- [ ] CDN cache invalidated (if needed)

## Deployment
- [ ] Blue-green deployment ready
- [ ] Health checks configured
- [ ] Resource limits set appropriately
- [ ] HPA configured and tested
- [ ] PDB ensures availability

## Post-Deployment
- [ ] Smoke tests passing
- [ ] Metrics baseline established
- [ ] Alerts configured and tested
- [ ] Error rates within SLO
- [ ] Latency within SLO

## Monitoring
- [ ] Dashboard accessible
- [ ] Logs flowing to central system
- [ ] Traces being collected
- [ ] On-call notified of deployment
```

---

## Quick Reference

### Distributed Systems Workflow
```
1. Architecture Design    → Distributed spec, CAP analysis
2. Event Design          → Kafka topics, schemas
3. Service Communication → gRPC/REST, resilience patterns
4. Async Processing      → Message queues, sagas
5. Dapr Integration      → State, pub/sub, bindings
6. CI/CD Pipeline        → Build, test, deploy
7. Observability         → Metrics, logs, traces
8. Production Deploy     → HA, security, monitoring
```

### Essential Commands
```bash
# Kafka
kafka-topics.sh --create --topic task-events --partitions 6
kafka-console-consumer.sh --topic task-events --from-beginning
kafka-consumer-groups.sh --describe --group task-processor

# Dapr
dapr run --app-id api --app-port 8000 -- python main.py
dapr publish --pubsub pubsub --topic task-events --data '{}'
dapr invoke --app-id api --method /tasks --verb GET

# Monitoring
kubectl port-forward svc/prometheus 9090:9090
kubectl port-forward svc/grafana 3000:3000
kubectl logs -f deployment/api -n todo-app

# Production
kubectl rollout status deployment/api
kubectl rollout undo deployment/api
kubectl top pods -n todo-app
```

### Key Specifications
| Spec | Purpose |
|------|---------|
| Distributed Architecture | System design, consistency |
| Kafka Topics | Event schemas, partitioning |
| Communication Matrix | Service interactions |
| CI/CD Pipeline | Automation workflow |
| Observability | Metrics, SLOs, alerts |
| Production Deployment | HA, security, DR |
