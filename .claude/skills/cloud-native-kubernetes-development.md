# Skill: Cloud-Native Kubernetes Application Development

A comprehensive skill for building, containerizing, and deploying applications to Kubernetes using Spec-Driven Development methodology with AI-assisted operations.

---

## 1. Cloud-Native Architecture Design

### Overview
Cloud-native applications are designed to fully exploit cloud computing advantages: scalability, resilience, manageability, and observability.

### Cloud-Native Principles
```
┌─────────────────────────────────────────────────────────┐
│              Cloud-Native 12-Factor App                  │
├─────────────────────────────────────────────────────────┤
│  1. Codebase      │ One codebase, many deploys          │
│  2. Dependencies  │ Explicitly declare and isolate      │
│  3. Config        │ Store in environment                │
│  4. Backing Svcs  │ Treat as attached resources         │
│  5. Build/Release │ Strictly separate stages            │
│  6. Processes     │ Execute as stateless processes      │
│  7. Port Binding  │ Export services via port binding    │
│  8. Concurrency   │ Scale out via process model         │
│  9. Disposability │ Fast startup, graceful shutdown     │
│ 10. Dev/Prod Par  │ Keep environments similar           │
│ 11. Logs          │ Treat as event streams              │
│ 12. Admin Procs   │ Run as one-off processes            │
└─────────────────────────────────────────────────────────┘
```

### Cloud-Native Architecture Specification
```markdown
# Cloud-Native Architecture Specification

## Application Identity
- **Name**: [Application Name]
- **Type**: [Microservice | Monolith | Serverless]
- **Domain**: [Business domain]

## Architecture Overview
```
                    ┌─────────────┐
                    │   Ingress   │
                    │  Controller │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
        ┌─────▼─────┐ ┌────▼────┐ ┌─────▼─────┐
        │ Frontend  │ │   API   │ │  Worker   │
        │  Service  │ │ Gateway │ │  Service  │
        └─────┬─────┘ └────┬────┘ └─────┬─────┘
              │            │            │
              └────────────┼────────────┘
                           │
                    ┌──────▼──────┐
                    │  Database   │
                    │  (Managed)  │
                    └─────────────┘
```

## Service Components

### Frontend Service
- **Type**: Web Application
- **Framework**: Next.js
- **Replicas**: 2-10 (HPA)
- **Resources**:
  - CPU: 100m-500m
  - Memory: 128Mi-512Mi

### API Service
- **Type**: REST API
- **Framework**: FastAPI
- **Replicas**: 2-10 (HPA)
- **Resources**:
  - CPU: 200m-1000m
  - Memory: 256Mi-1Gi

### Worker Service
- **Type**: Background Jobs
- **Framework**: Celery/Custom
- **Replicas**: 1-5
- **Resources**:
  - CPU: 100m-500m
  - Memory: 256Mi-512Mi

## Infrastructure Requirements

### Compute
- **Cluster**: Kubernetes 1.28+
- **Node Pool**: 3 nodes minimum
- **Instance Type**: 2 vCPU, 4GB RAM

### Storage
- **Database**: PostgreSQL (managed)
- **Cache**: Redis (managed)
- **Object Storage**: S3-compatible

### Networking
- **Ingress**: NGINX Ingress Controller
- **TLS**: cert-manager with Let's Encrypt
- **DNS**: External DNS controller

## Non-Functional Requirements

### Availability
- **SLA Target**: 99.9%
- **Strategy**: Multi-replica, health checks
- **Failover**: Automatic pod rescheduling

### Scalability
- **Horizontal**: HPA based on CPU/memory
- **Vertical**: VPA for resource optimization
- **Scaling Triggers**: 70% CPU, 80% memory

### Security
- **Network Policies**: Namespace isolation
- **Secrets**: External Secrets Operator
- **RBAC**: Least privilege access
- **Pod Security**: Restricted standards
```

### Microservices Communication Patterns
```yaml
# Service Communication Specification
communication:
  synchronous:
    - pattern: REST
      use_case: User-facing requests
      timeout: 30s
      retry: 3x with exponential backoff

    - pattern: gRPC
      use_case: Internal service-to-service
      timeout: 10s
      retry: 3x

  asynchronous:
    - pattern: Message Queue
      broker: Redis/RabbitMQ
      use_case: Background jobs
      delivery: At-least-once

    - pattern: Event Streaming
      broker: Kafka
      use_case: Event sourcing, audit logs
      delivery: Exactly-once

  service_discovery:
    method: Kubernetes DNS
    format: <service>.<namespace>.svc.cluster.local
```

---

## 2. Containerization via Specs

### Container Specification Template
```markdown
# Container Specification: [Service Name]

## Base Image
- **Image**: python:3.11-slim
- **Rationale**: Minimal size, security patches

## Build Stages
1. **Dependencies**: Install pip packages
2. **Application**: Copy source code
3. **Runtime**: Configure entrypoint

## Environment Variables
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| DATABASE_URL | Yes | - | PostgreSQL connection |
| REDIS_URL | No | localhost:6379 | Cache connection |
| LOG_LEVEL | No | INFO | Logging verbosity |

## Ports
| Port | Protocol | Description |
|------|----------|-------------|
| 8000 | HTTP | API endpoint |
| 9090 | HTTP | Metrics endpoint |

## Health Checks
- **Liveness**: GET /health/live
- **Readiness**: GET /health/ready
- **Startup**: GET /health/startup

## Resource Limits
- **CPU**: 100m request, 500m limit
- **Memory**: 128Mi request, 512Mi limit

## Security
- **User**: Non-root (UID 1000)
- **Filesystem**: Read-only root
- **Capabilities**: Drop all
```

### Multi-Stage Dockerfile (Python/FastAPI)
```dockerfile
# Dockerfile
# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim AS production

# Security: Run as non-root user
RUN groupadd -r appgroup && useradd -r -g appgroup appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY --chown=appuser:appgroup ./app ./app

# Security: Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/live')" || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Multi-Stage Dockerfile (Node.js/Next.js)
```dockerfile
# Dockerfile
# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm ci --only=production

# Stage 2: Build
FROM node:20-alpine AS builder
WORKDIR /app

COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build application
ENV NEXT_TELEMETRY_DISABLED=1
RUN npm run build

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

# Security: Run as non-root
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copy built application
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

# Security: Set ownership
RUN chown -R nextjs:nodejs /app

USER nextjs

EXPOSE 3000
ENV PORT=3000
ENV HOSTNAME="0.0.0.0"

CMD ["node", "server.js"]
```

### Docker Compose for Local Development
```yaml
# docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - api

  api:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/app
      - REDIS_URL=redis://redis:6379
    depends_on:
      - db
      - redis

  db:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: app
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Container Build Specification
```yaml
# build-spec.yaml
version: "1.0"
services:
  api:
    context: ./backend
    dockerfile: Dockerfile
    image: ${REGISTRY}/api:${VERSION}
    platforms:
      - linux/amd64
      - linux/arm64
    build_args:
      PYTHON_VERSION: "3.11"
    labels:
      maintainer: "team@example.com"
      version: "${VERSION}"
    scan: true
    push: true

  frontend:
    context: ./frontend
    dockerfile: Dockerfile
    image: ${REGISTRY}/frontend:${VERSION}
    platforms:
      - linux/amd64
      - linux/arm64
    build_args:
      NODE_VERSION: "20"
    labels:
      maintainer: "team@example.com"
      version: "${VERSION}"
    scan: true
    push: true

registry:
  url: ghcr.io/myorg
  auth:
    method: token
    secret: GITHUB_TOKEN

scanning:
  tool: trivy
  severity: HIGH,CRITICAL
  fail_on_vulnerability: true
```

---

## 3. Kubernetes Basics (Pods, Services, Deployments)

### Kubernetes Resource Hierarchy
```
┌─────────────────────────────────────────────────────────┐
│                      Cluster                             │
├─────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────┐   │
│  │                   Namespace                      │   │
│  ├─────────────────────────────────────────────────┤   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐   │   │
│  │  │Deployment │  │  Service  │  │  Ingress  │   │   │
│  │  ├───────────┤  ├───────────┤  ├───────────┤   │   │
│  │  │ ReplicaSet│  │ClusterIP  │  │   Rules   │   │   │
│  │  ├───────────┤  │NodePort   │  │   Paths   │   │   │
│  │  │   Pods    │  │LoadBalancer│  │   TLS    │   │   │
│  │  └───────────┘  └───────────┘  └───────────┘   │   │
│  │                                                  │   │
│  │  ┌───────────┐  ┌───────────┐  ┌───────────┐   │   │
│  │  │ConfigMap  │  │  Secret   │  │    PVC    │   │   │
│  │  └───────────┘  └───────────┘  └───────────┘   │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Namespace Specification
```yaml
# namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/env: production
  annotations:
    description: "Todo application namespace"
```

### Pod Specification
```yaml
# pod.yaml (for reference - use Deployments in production)
apiVersion: v1
kind: Pod
metadata:
  name: api-pod
  namespace: todo-app
  labels:
    app: api
    version: v1
spec:
  securityContext:
    runAsNonRoot: true
    runAsUser: 1000
    fsGroup: 1000

  containers:
    - name: api
      image: ghcr.io/myorg/api:v1.0.0
      imagePullPolicy: IfNotPresent

      ports:
        - name: http
          containerPort: 8000
          protocol: TCP
        - name: metrics
          containerPort: 9090
          protocol: TCP

      env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-credentials
              key: url
        - name: LOG_LEVEL
          valueFrom:
            configMapKeyRef:
              name: api-config
              key: log_level

      resources:
        requests:
          cpu: 100m
          memory: 128Mi
        limits:
          cpu: 500m
          memory: 512Mi

      securityContext:
        allowPrivilegeEscalation: false
        readOnlyRootFilesystem: true
        capabilities:
          drop:
            - ALL

      livenessProbe:
        httpGet:
          path: /health/live
          port: http
        initialDelaySeconds: 10
        periodSeconds: 15
        timeoutSeconds: 5
        failureThreshold: 3

      readinessProbe:
        httpGet:
          path: /health/ready
          port: http
        initialDelaySeconds: 5
        periodSeconds: 10
        timeoutSeconds: 5
        failureThreshold: 3

      startupProbe:
        httpGet:
          path: /health/startup
          port: http
        initialDelaySeconds: 0
        periodSeconds: 5
        timeoutSeconds: 5
        failureThreshold: 30

      volumeMounts:
        - name: tmp
          mountPath: /tmp
        - name: cache
          mountPath: /app/.cache

  volumes:
    - name: tmp
      emptyDir: {}
    - name: cache
      emptyDir: {}

  restartPolicy: Always
```

### Deployment Specification
```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api
  namespace: todo-app
  labels:
    app.kubernetes.io/name: api
    app.kubernetes.io/component: backend
    app.kubernetes.io/version: "1.0.0"
spec:
  replicas: 3
  revisionHistoryLimit: 5

  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 0

  selector:
    matchLabels:
      app.kubernetes.io/name: api

  template:
    metadata:
      labels:
        app.kubernetes.io/name: api
        app.kubernetes.io/component: backend
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "9090"
        prometheus.io/path: "/metrics"
    spec:
      serviceAccountName: api-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
        seccompProfile:
          type: RuntimeDefault

      affinity:
        podAntiAffinity:
          preferredDuringSchedulingIgnoredDuringExecution:
            - weight: 100
              podAffinityTerm:
                labelSelector:
                  matchLabels:
                    app.kubernetes.io/name: api
                topologyKey: kubernetes.io/hostname

      containers:
        - name: api
          image: ghcr.io/myorg/api:v1.0.0
          imagePullPolicy: IfNotPresent

          ports:
            - name: http
              containerPort: 8000
            - name: metrics
              containerPort: 9090

          envFrom:
            - configMapRef:
                name: api-config
            - secretRef:
                name: api-secrets

          resources:
            requests:
              cpu: 100m
              memory: 128Mi
            limits:
              cpu: 500m
              memory: 512Mi

          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL

          livenessProbe:
            httpGet:
              path: /health/live
              port: http
            initialDelaySeconds: 10
            periodSeconds: 15

          readinessProbe:
            httpGet:
              path: /health/ready
              port: http
            initialDelaySeconds: 5
            periodSeconds: 10

          volumeMounts:
            - name: tmp
              mountPath: /tmp

      volumes:
        - name: tmp
          emptyDir: {}

      terminationGracePeriodSeconds: 30

---
# Horizontal Pod Autoscaler
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: Resource
      resource:
        name: cpu
        target:
          type: Utilization
          averageUtilization: 70
    - type: Resource
      resource:
        name: memory
        target:
          type: Utilization
          averageUtilization: 80
  behavior:
    scaleUp:
      stabilizationWindowSeconds: 60
      policies:
        - type: Pods
          value: 2
          periodSeconds: 60
    scaleDown:
      stabilizationWindowSeconds: 300
      policies:
        - type: Percent
          value: 10
          periodSeconds: 60
```

### Service Specification
```yaml
# service.yaml
apiVersion: v1
kind: Service
metadata:
  name: api
  namespace: todo-app
  labels:
    app.kubernetes.io/name: api
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: api
  ports:
    - name: http
      port: 80
      targetPort: 8000
      protocol: TCP
    - name: metrics
      port: 9090
      targetPort: 9090
      protocol: TCP

---
# Headless service for StatefulSets
apiVersion: v1
kind: Service
metadata:
  name: api-headless
  namespace: todo-app
spec:
  type: ClusterIP
  clusterIP: None
  selector:
    app.kubernetes.io/name: api
  ports:
    - name: http
      port: 8000
```

### Ingress Specification
```yaml
# ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-app-ingress
  namespace: todo-app
  annotations:
    kubernetes.io/ingress.class: nginx
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/proxy-body-size: "10m"
    nginx.ingress.kubernetes.io/rate-limit: "100"
    nginx.ingress.kubernetes.io/rate-limit-window: "1m"
spec:
  tls:
    - hosts:
        - app.example.com
        - api.example.com
      secretName: todo-app-tls

  rules:
    - host: app.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: frontend
                port:
                  number: 80

    - host: api.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: api
                port:
                  number: 80
```

### ConfigMap and Secret
```yaml
# configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: api-config
  namespace: todo-app
data:
  LOG_LEVEL: "INFO"
  CORS_ORIGINS: "https://app.example.com"
  RATE_LIMIT: "100"

---
# secret.yaml (use External Secrets in production)
apiVersion: v1
kind: Secret
metadata:
  name: api-secrets
  namespace: todo-app
type: Opaque
stringData:
  DATABASE_URL: "postgresql://user:pass@db:5432/app"
  JWT_SECRET: "your-jwt-secret"
  REDIS_URL: "redis://redis:6379"
```

---

## 4. Helm Chart Specification

### Helm Chart Structure
```
charts/todo-app/
├── Chart.yaml              # Chart metadata
├── values.yaml             # Default values
├── values-dev.yaml         # Development overrides
├── values-prod.yaml        # Production overrides
├── templates/
│   ├── _helpers.tpl        # Template helpers
│   ├── namespace.yaml      # Namespace
│   ├── deployment.yaml     # Deployments
│   ├── service.yaml        # Services
│   ├── ingress.yaml        # Ingress
│   ├── configmap.yaml      # ConfigMaps
│   ├── secret.yaml         # Secrets
│   ├── hpa.yaml           # Autoscaling
│   ├── pdb.yaml           # Pod Disruption Budget
│   ├── serviceaccount.yaml # Service Account
│   └── NOTES.txt          # Post-install notes
└── charts/                 # Subcharts (dependencies)
```

### Chart.yaml
```yaml
# Chart.yaml
apiVersion: v2
name: todo-app
description: A Helm chart for the Todo Application
type: application
version: 1.0.0
appVersion: "1.0.0"

keywords:
  - todo
  - task-management
  - fastapi
  - nextjs

maintainers:
  - name: DevOps Team
    email: devops@example.com

dependencies:
  - name: postgresql
    version: "12.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: postgresql.enabled

  - name: redis
    version: "17.x.x"
    repository: "https://charts.bitnami.com/bitnami"
    condition: redis.enabled
```

### values.yaml
```yaml
# values.yaml
global:
  imageRegistry: ghcr.io/myorg
  imagePullSecrets:
    - name: regcred
  storageClass: standard

# API Service
api:
  enabled: true
  replicaCount: 2

  image:
    repository: api
    tag: "latest"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 80
    targetPort: 8000

  resources:
    requests:
      cpu: 100m
      memory: 128Mi
    limits:
      cpu: 500m
      memory: 512Mi

  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilization: 70
    targetMemoryUtilization: 80

  env:
    LOG_LEVEL: INFO

  secrets:
    DATABASE_URL: ""
    JWT_SECRET: ""

  probes:
    liveness:
      path: /health/live
      initialDelaySeconds: 10
      periodSeconds: 15
    readiness:
      path: /health/ready
      initialDelaySeconds: 5
      periodSeconds: 10

  nodeSelector: {}
  tolerations: []
  affinity: {}

# Frontend Service
frontend:
  enabled: true
  replicaCount: 2

  image:
    repository: frontend
    tag: "latest"
    pullPolicy: IfNotPresent

  service:
    type: ClusterIP
    port: 80
    targetPort: 3000

  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 256Mi

  env:
    NEXT_PUBLIC_API_URL: "https://api.example.com"

# Ingress Configuration
ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
  hosts:
    - host: app.example.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
    - host: api.example.com
      paths:
        - path: /
          pathType: Prefix
          service: api
  tls:
    - secretName: todo-app-tls
      hosts:
        - app.example.com
        - api.example.com

# PostgreSQL (Bitnami subchart)
postgresql:
  enabled: true
  auth:
    username: todoapp
    password: ""
    database: todoapp
  primary:
    persistence:
      size: 10Gi

# Redis (Bitnami subchart)
redis:
  enabled: true
  auth:
    enabled: false
  master:
    persistence:
      size: 1Gi

# Service Account
serviceAccount:
  create: true
  name: ""
  annotations: {}

# Pod Disruption Budget
podDisruptionBudget:
  enabled: true
  minAvailable: 1

# Network Policy
networkPolicy:
  enabled: false

# Monitoring
metrics:
  enabled: true
  serviceMonitor:
    enabled: false
```

### Deployment Template
```yaml
# templates/deployment.yaml
{{- if .Values.api.enabled }}
apiVersion: apps/v1
kind: Deployment
metadata:
  name: {{ include "todo-app.fullname" . }}-api
  namespace: {{ .Release.Namespace }}
  labels:
    {{- include "todo-app.labels" . | nindent 4 }}
    app.kubernetes.io/component: api
spec:
  {{- if not .Values.api.autoscaling.enabled }}
  replicas: {{ .Values.api.replicaCount }}
  {{- end }}
  selector:
    matchLabels:
      {{- include "todo-app.selectorLabels" . | nindent 6 }}
      app.kubernetes.io/component: api
  template:
    metadata:
      annotations:
        checksum/config: {{ include (print $.Template.BasePath "/configmap.yaml") . | sha256sum }}
        checksum/secret: {{ include (print $.Template.BasePath "/secret.yaml") . | sha256sum }}
      labels:
        {{- include "todo-app.selectorLabels" . | nindent 8 }}
        app.kubernetes.io/component: api
    spec:
      {{- with .Values.global.imagePullSecrets }}
      imagePullSecrets:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      serviceAccountName: {{ include "todo-app.serviceAccountName" . }}
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
        - name: api
          image: "{{ .Values.global.imageRegistry }}/{{ .Values.api.image.repository }}:{{ .Values.api.image.tag | default .Chart.AppVersion }}"
          imagePullPolicy: {{ .Values.api.image.pullPolicy }}
          ports:
            - name: http
              containerPort: {{ .Values.api.service.targetPort }}
              protocol: TCP
          envFrom:
            - configMapRef:
                name: {{ include "todo-app.fullname" . }}-api
            - secretRef:
                name: {{ include "todo-app.fullname" . }}-api
          {{- with .Values.api.env }}
          env:
            {{- range $key, $value := . }}
            - name: {{ $key }}
              value: {{ $value | quote }}
            {{- end }}
          {{- end }}
          resources:
            {{- toYaml .Values.api.resources | nindent 12 }}
          securityContext:
            allowPrivilegeEscalation: false
            readOnlyRootFilesystem: true
            capabilities:
              drop:
                - ALL
          livenessProbe:
            httpGet:
              path: {{ .Values.api.probes.liveness.path }}
              port: http
            initialDelaySeconds: {{ .Values.api.probes.liveness.initialDelaySeconds }}
            periodSeconds: {{ .Values.api.probes.liveness.periodSeconds }}
          readinessProbe:
            httpGet:
              path: {{ .Values.api.probes.readiness.path }}
              port: http
            initialDelaySeconds: {{ .Values.api.probes.readiness.initialDelaySeconds }}
            periodSeconds: {{ .Values.api.probes.readiness.periodSeconds }}
          volumeMounts:
            - name: tmp
              mountPath: /tmp
      volumes:
        - name: tmp
          emptyDir: {}
      {{- with .Values.api.nodeSelector }}
      nodeSelector:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.api.affinity }}
      affinity:
        {{- toYaml . | nindent 8 }}
      {{- end }}
      {{- with .Values.api.tolerations }}
      tolerations:
        {{- toYaml . | nindent 8 }}
      {{- end }}
{{- end }}
```

### Helper Templates
```yaml
# templates/_helpers.tpl
{{/*
Expand the name of the chart.
*/}}
{{- define "todo-app.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
*/}}
{{- define "todo-app.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "todo-app.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "todo-app.labels" -}}
helm.sh/chart: {{ include "todo-app.chart" . }}
{{ include "todo-app.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "todo-app.selectorLabels" -}}
app.kubernetes.io/name: {{ include "todo-app.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "todo-app.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "todo-app.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}
```

---

## 5. Local Cluster Management (Minikube)

### Minikube Setup Specification
```markdown
# Local Kubernetes Development Setup

## Prerequisites
- Docker Desktop or compatible runtime
- 8GB+ RAM available
- 20GB+ disk space

## Minikube Configuration
- **Driver**: docker (recommended)
- **Kubernetes**: v1.28+
- **CPUs**: 4
- **Memory**: 8192MB
- **Disk**: 40GB

## Required Addons
- ingress (NGINX)
- metrics-server
- dashboard
- registry
```

### Minikube Setup Script
```bash
#!/bin/bash
# scripts/setup-minikube.sh

set -e

echo "Setting up Minikube cluster..."

# Start Minikube with recommended settings
minikube start \
  --driver=docker \
  --cpus=4 \
  --memory=8192 \
  --disk-size=40g \
  --kubernetes-version=v1.28.0 \
  --addons=ingress,metrics-server,dashboard

# Wait for cluster to be ready
echo "Waiting for cluster to be ready..."
kubectl wait --for=condition=Ready nodes --all --timeout=120s

# Enable additional addons
minikube addons enable registry
minikube addons enable ingress-dns

# Configure local registry
echo "Configuring local registry..."
eval $(minikube docker-env)

# Create development namespace
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -

# Set default namespace
kubectl config set-context --current --namespace=dev

echo "Minikube setup complete!"
echo ""
echo "Useful commands:"
echo "  minikube dashboard    - Open Kubernetes dashboard"
echo "  minikube tunnel       - Expose LoadBalancer services"
echo "  minikube ip           - Get cluster IP"
echo "  eval \$(minikube docker-env) - Use Minikube's Docker"
```

### Local Development Workflow
```bash
#!/bin/bash
# scripts/dev-workflow.sh

# 1. Start Minikube (if not running)
minikube status || minikube start

# 2. Use Minikube's Docker daemon
eval $(minikube docker-env)

# 3. Build images locally (no push needed)
docker build -t todo-api:dev ./backend
docker build -t todo-frontend:dev ./frontend

# 4. Deploy with Helm (development values)
helm upgrade --install todo-app ./charts/todo-app \
  --namespace dev \
  --create-namespace \
  -f ./charts/todo-app/values-dev.yaml \
  --set api.image.tag=dev \
  --set frontend.image.tag=dev

# 5. Wait for deployment
kubectl rollout status deployment/todo-app-api -n dev
kubectl rollout status deployment/todo-app-frontend -n dev

# 6. Start tunnel for ingress access
echo "Starting Minikube tunnel (requires sudo)..."
minikube tunnel
```

### Development Values Override
```yaml
# values-dev.yaml
global:
  imageRegistry: ""  # Use local images
  imagePullSecrets: []

api:
  replicaCount: 1
  image:
    repository: todo-api
    tag: dev
    pullPolicy: Never  # Use local images

  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 500m
      memory: 512Mi

  autoscaling:
    enabled: false

  env:
    LOG_LEVEL: DEBUG
    DEBUG: "true"

frontend:
  replicaCount: 1
  image:
    repository: todo-frontend
    tag: dev
    pullPolicy: Never

  resources:
    requests:
      cpu: 50m
      memory: 64Mi
    limits:
      cpu: 200m
      memory: 256Mi

  env:
    NEXT_PUBLIC_API_URL: "http://api.todo.local"

ingress:
  enabled: true
  className: nginx
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "false"
  hosts:
    - host: todo.local
      paths:
        - path: /
          pathType: Prefix
          service: frontend
    - host: api.todo.local
      paths:
        - path: /
          pathType: Prefix
          service: api
  tls: []  # No TLS in dev

postgresql:
  enabled: true
  auth:
    password: devpassword
  primary:
    persistence:
      size: 1Gi

redis:
  enabled: true
  master:
    persistence:
      size: 100Mi

podDisruptionBudget:
  enabled: false

metrics:
  enabled: false
```

### Minikube Commands Reference
```bash
# Cluster Management
minikube start                    # Start cluster
minikube stop                     # Stop cluster
minikube delete                   # Delete cluster
minikube status                   # Check status
minikube ip                       # Get cluster IP

# Addons
minikube addons list              # List all addons
minikube addons enable <addon>    # Enable addon
minikube addons disable <addon>   # Disable addon

# Docker Integration
eval $(minikube docker-env)       # Use Minikube's Docker
eval $(minikube docker-env -u)    # Revert to host Docker

# Networking
minikube tunnel                   # Expose LoadBalancer services
minikube service <name> --url     # Get service URL

# Dashboard
minikube dashboard                # Open web dashboard

# Troubleshooting
minikube logs                     # View logs
minikube ssh                      # SSH into node
kubectl get events --sort-by='.lastTimestamp'  # Recent events
```

---

## 6. AI-Assisted Ops (kubectl-ai, kagent)

### kubectl-ai Overview
```markdown
# kubectl-ai: Natural Language Kubernetes Operations

## Overview
kubectl-ai enables natural language interactions with Kubernetes clusters,
translating human requests into kubectl commands.

## Use Cases
- Quick resource queries
- Debugging assistance
- Learning kubectl syntax
- Complex query construction

## Safety
- Preview mode by default
- Confirmation required for mutations
- Audit logging enabled
```

### kubectl-ai Installation & Setup
```bash
# Install kubectl-ai
brew install kubectl-ai  # macOS
# or
go install github.com/sozercan/kubectl-ai@latest

# Configure
export OPENAI_API_KEY="your-api-key"

# Optional: Use local models
kubectl ai --backend ollama --model llama2
```

### kubectl-ai Usage Examples
```bash
# Querying Resources
kubectl ai "show all pods that are not running"
# Generated: kubectl get pods -A --field-selector=status.phase!=Running

kubectl ai "find pods using more than 500Mi memory"
# Generated: kubectl top pods -A | awk '$4 > 500'

kubectl ai "list services exposed externally"
# Generated: kubectl get svc -A --field-selector spec.type=LoadBalancer

# Debugging
kubectl ai "why is my pod crashing"
# Generated: kubectl describe pod <name> && kubectl logs <name> --previous

kubectl ai "show events for failing deployments"
# Generated: kubectl get events --field-selector reason=Failed

# Operations (with confirmation)
kubectl ai "scale deployment api to 5 replicas"
# Preview: kubectl scale deployment api --replicas=5
# Confirm? [y/N]

kubectl ai "restart all pods in namespace todo-app"
# Preview: kubectl rollout restart deployment -n todo-app
# Confirm? [y/N]
```

### kagent: Kubernetes AI Agent
```markdown
# kagent: Autonomous Kubernetes Management Agent

## Overview
kagent is an AI agent that can autonomously manage Kubernetes resources,
perform diagnostics, and execute remediation actions.

## Capabilities
- Health monitoring and alerting
- Automatic scaling decisions
- Resource optimization
- Incident response

## Safety Controls
- Action approval workflow
- Rollback capabilities
- Audit trail
- Scope limitations
```

### kagent Configuration
```yaml
# kagent-config.yaml
apiVersion: kagent.io/v1
kind: AgentConfig
metadata:
  name: todo-app-agent
  namespace: kagent-system
spec:
  # Target namespace
  scope:
    namespaces:
      - todo-app
    resources:
      - deployments
      - pods
      - services
      - hpa

  # AI Model Configuration
  model:
    provider: openai
    name: gpt-4
    temperature: 0.1

  # Safety Controls
  safety:
    requireApproval:
      - delete
      - scale
      - restart
    maxActionsPerHour: 10
    dryRunDefault: true

  # Monitoring Rules
  monitoring:
    - name: pod-crash-loop
      condition: "pod.restartCount > 3"
      action: diagnose

    - name: high-cpu
      condition: "pod.cpuUsage > 90%"
      action: suggest-scaling

    - name: oom-killed
      condition: "pod.lastTerminationReason == 'OOMKilled'"
      action: suggest-resource-increase

  # Notification Channels
  notifications:
    slack:
      channel: "#k8s-alerts"
      events:
        - action-suggested
        - action-approved
        - action-executed
```

### AI-Assisted Debugging Workflow
```python
# scripts/ai_debug.py
"""AI-assisted Kubernetes debugging workflow."""

import subprocess
import json
from openai import OpenAI

client = OpenAI()

def get_pod_status(namespace: str) -> dict:
    """Get pod status from cluster."""
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", namespace, "-o", "json"],
        capture_output=True, text=True
    )
    return json.loads(result.stdout)

def get_pod_logs(pod: str, namespace: str) -> str:
    """Get pod logs."""
    result = subprocess.run(
        ["kubectl", "logs", pod, "-n", namespace, "--tail=100"],
        capture_output=True, text=True
    )
    return result.stdout

def get_pod_events(pod: str, namespace: str) -> str:
    """Get events for a pod."""
    result = subprocess.run(
        ["kubectl", "get", "events", "-n", namespace,
         f"--field-selector=involvedObject.name={pod}"],
        capture_output=True, text=True
    )
    return result.stdout

def diagnose_pod(pod: str, namespace: str) -> str:
    """Use AI to diagnose pod issues."""
    # Gather context
    status = get_pod_status(namespace)
    logs = get_pod_logs(pod, namespace)
    events = get_pod_events(pod, namespace)

    # Ask AI for diagnosis
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": """You are a Kubernetes debugging expert.
                Analyze the provided pod information and:
                1. Identify the root cause of any issues
                2. Suggest specific remediation steps
                3. Provide kubectl commands to fix the issue
                Be concise and actionable."""
            },
            {
                "role": "user",
                "content": f"""Diagnose this pod:

                Pod Status:
                {json.dumps(status, indent=2)}

                Recent Logs:
                {logs}

                Events:
                {events}
                """
            }
        ]
    )

    return response.choices[0].message.content

# Example usage
if __name__ == "__main__":
    diagnosis = diagnose_pod("api-5d8c9f7b6-x9j2k", "todo-app")
    print(diagnosis)
```

### AI Ops Specification
```markdown
# AI Operations Specification

## Allowed Autonomous Actions
| Action | Conditions | Approval |
|--------|------------|----------|
| Pod restart | CrashLoopBackOff > 5min | Auto |
| HPA adjustment | CPU > 90% for 5min | Auto |
| Log collection | Any pod failure | Auto |
| Resource scaling | Memory > 85% | Manual |
| Deployment rollback | Error rate > 5% | Manual |
| Node drain | Node unhealthy | Manual |

## Prohibited Actions
- Namespace deletion
- Secret modification
- RBAC changes
- Network policy changes
- PV/PVC deletion

## Audit Requirements
- All actions logged to audit system
- Slack notification for manual approvals
- Weekly report of automated actions
- Rollback capability for 24 hours

## Escalation Path
1. AI suggests action
2. If auto-approved: execute with monitoring
3. If manual: notify on-call engineer
4. If no response in 15min: escalate to team lead
```

---

## 7. Infrastructure as Specification

### Infrastructure Specification Template
```markdown
# Infrastructure Specification: [Environment Name]

## Environment Overview
- **Name**: production
- **Region**: us-east-1
- **Cloud Provider**: AWS/GCP/Azure

## Cluster Specification

### Control Plane
- **Type**: Managed (EKS/GKE/AKS)
- **Version**: 1.28
- **High Availability**: Yes (3 AZ)

### Node Pools

#### Default Pool
- **Instance Type**: t3.large (2 vCPU, 8GB)
- **Min Nodes**: 3
- **Max Nodes**: 10
- **Autoscaling**: Enabled

#### High-Memory Pool
- **Instance Type**: r6i.xlarge (4 vCPU, 32GB)
- **Min Nodes**: 0
- **Max Nodes**: 5
- **Taints**: workload=memory:NoSchedule

## Networking
- **VPC CIDR**: 10.0.0.0/16
- **Pod CIDR**: 10.1.0.0/16
- **Service CIDR**: 10.2.0.0/16
- **DNS**: CoreDNS

## Storage
- **Default StorageClass**: gp3
- **Backup**: Daily snapshots, 7-day retention

## Security
- **Network Policies**: Calico
- **Secrets Management**: External Secrets + Vault
- **Pod Security**: Restricted
- **Audit Logging**: CloudWatch/Stackdriver

## Observability
- **Metrics**: Prometheus + Grafana
- **Logging**: Loki/ELK
- **Tracing**: Jaeger
- **Alerting**: AlertManager → PagerDuty
```

### Pulumi Infrastructure (Python)
```python
# infrastructure/main.py
"""Infrastructure as Code using Pulumi."""

import pulumi
from pulumi_kubernetes import Provider
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.core.v1 import Namespace, Service, ConfigMap, Secret
from pulumi_kubernetes.networking.v1 import Ingress

# Configuration
config = pulumi.Config()
env = config.require("environment")
app_name = "todo-app"

# Create namespace
namespace = Namespace(
    f"{app_name}-namespace",
    metadata={
        "name": f"{app_name}-{env}",
        "labels": {
            "app.kubernetes.io/name": app_name,
            "app.kubernetes.io/env": env,
        }
    }
)

# ConfigMap
api_config = ConfigMap(
    f"{app_name}-api-config",
    metadata={
        "name": "api-config",
        "namespace": namespace.metadata.name,
    },
    data={
        "LOG_LEVEL": "INFO" if env == "production" else "DEBUG",
        "CORS_ORIGINS": config.require("cors_origins"),
    }
)

# Secret (reference from external source in production)
api_secret = Secret(
    f"{app_name}-api-secret",
    metadata={
        "name": "api-secrets",
        "namespace": namespace.metadata.name,
    },
    string_data={
        "DATABASE_URL": config.require_secret("database_url"),
        "JWT_SECRET": config.require_secret("jwt_secret"),
    }
)

# API Deployment
api_deployment = Deployment(
    f"{app_name}-api",
    metadata={
        "name": "api",
        "namespace": namespace.metadata.name,
        "labels": {
            "app.kubernetes.io/name": "api",
            "app.kubernetes.io/component": "backend",
        }
    },
    spec={
        "replicas": 3 if env == "production" else 1,
        "selector": {
            "matchLabels": {
                "app.kubernetes.io/name": "api",
            }
        },
        "template": {
            "metadata": {
                "labels": {
                    "app.kubernetes.io/name": "api",
                }
            },
            "spec": {
                "containers": [{
                    "name": "api",
                    "image": f"{config.require('registry')}/api:{config.require('version')}",
                    "ports": [{"containerPort": 8000}],
                    "envFrom": [
                        {"configMapRef": {"name": api_config.metadata.name}},
                        {"secretRef": {"name": api_secret.metadata.name}},
                    ],
                    "resources": {
                        "requests": {"cpu": "100m", "memory": "128Mi"},
                        "limits": {"cpu": "500m", "memory": "512Mi"},
                    },
                    "livenessProbe": {
                        "httpGet": {"path": "/health/live", "port": 8000},
                        "initialDelaySeconds": 10,
                        "periodSeconds": 15,
                    },
                    "readinessProbe": {
                        "httpGet": {"path": "/health/ready", "port": 8000},
                        "initialDelaySeconds": 5,
                        "periodSeconds": 10,
                    },
                }],
            }
        }
    }
)

# API Service
api_service = Service(
    f"{app_name}-api-service",
    metadata={
        "name": "api",
        "namespace": namespace.metadata.name,
    },
    spec={
        "selector": {"app.kubernetes.io/name": "api"},
        "ports": [{"port": 80, "targetPort": 8000}],
        "type": "ClusterIP",
    }
)

# Ingress
ingress = Ingress(
    f"{app_name}-ingress",
    metadata={
        "name": "todo-ingress",
        "namespace": namespace.metadata.name,
        "annotations": {
            "kubernetes.io/ingress.class": "nginx",
            "cert-manager.io/cluster-issuer": "letsencrypt-prod",
        }
    },
    spec={
        "tls": [{
            "hosts": [config.require("api_host")],
            "secretName": "api-tls",
        }],
        "rules": [{
            "host": config.require("api_host"),
            "http": {
                "paths": [{
                    "path": "/",
                    "pathType": "Prefix",
                    "backend": {
                        "service": {
                            "name": api_service.metadata.name,
                            "port": {"number": 80},
                        }
                    }
                }]
            }
        }]
    }
)

# Exports
pulumi.export("namespace", namespace.metadata.name)
pulumi.export("api_service", api_service.metadata.name)
pulumi.export("ingress_host", config.require("api_host"))
```

### GitOps with ArgoCD
```yaml
# argocd/application.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: todo-app
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default

  source:
    repoURL: https://github.com/myorg/todo-app.git
    targetRevision: main
    path: charts/todo-app
    helm:
      valueFiles:
        - values.yaml
        - values-prod.yaml
      parameters:
        - name: api.image.tag
          value: $ARGOCD_APP_REVISION

  destination:
    server: https://kubernetes.default.svc
    namespace: todo-app

  syncPolicy:
    automated:
      prune: true
      selfHeal: true
      allowEmpty: false
    syncOptions:
      - CreateNamespace=true
      - PrunePropagationPolicy=foreground
      - PruneLast=true
    retry:
      limit: 5
      backoff:
        duration: 5s
        factor: 2
        maxDuration: 3m

  ignoreDifferences:
    - group: apps
      kind: Deployment
      jsonPointers:
        - /spec/replicas  # Managed by HPA
```

### CI/CD Pipeline Specification
```yaml
# .github/workflows/deploy.yaml
name: Build and Deploy

on:
  push:
    branches: [main]
    tags: ['v*']
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run tests
        run: |
          cd backend && python -m pytest tests/ -v
          cd ../frontend && npm test

  build:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=sha

      - name: Build and push API
        uses: docker/build-push-action@v5
        with:
          context: ./backend
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/api:${{ steps.meta.outputs.version }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

      - name: Build and push Frontend
        uses: docker/build-push-action@v5
        with:
          context: ./frontend
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:${{ steps.meta.outputs.version }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    needs: build
    if: github.ref == 'refs/heads/main' || startsWith(github.ref, 'refs/tags/v')
    runs-on: ubuntu-latest
    environment: production

    steps:
      - uses: actions/checkout@v4

      - name: Install Helm
        uses: azure/setup-helm@v3

      - name: Configure Kubernetes
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBE_CONFIG }}

      - name: Deploy with Helm
        run: |
          helm upgrade --install todo-app ./charts/todo-app \
            --namespace todo-app \
            --create-namespace \
            -f ./charts/todo-app/values-prod.yaml \
            --set api.image.tag=${{ github.sha }} \
            --set frontend.image.tag=${{ github.sha }} \
            --wait --timeout 10m

      - name: Verify deployment
        run: |
          kubectl rollout status deployment/todo-app-api -n todo-app
          kubectl rollout status deployment/todo-app-frontend -n todo-app
```

---

## Quick Reference

### Cloud-Native Development Workflow
```
1. Define Architecture     → Infrastructure Spec
2. Containerize           → Dockerfile + Build Spec
3. Create K8s Manifests   → Deployment, Service, Ingress
4. Package with Helm      → Chart + Values
5. Local Testing          → Minikube + dev values
6. CI/CD Pipeline         → GitHub Actions + ArgoCD
7. Production Deploy      → GitOps sync
```

### Essential Commands
```bash
# Minikube
minikube start
minikube dashboard
minikube tunnel
eval $(minikube docker-env)

# Docker
docker build -t app:tag .
docker run -p 8000:8000 app:tag

# Kubernetes
kubectl apply -f manifest.yaml
kubectl get pods -n namespace
kubectl logs pod-name
kubectl describe pod pod-name
kubectl port-forward svc/api 8000:80

# Helm
helm install app ./chart
helm upgrade app ./chart -f values.yaml
helm list
helm rollback app 1

# AI-Assisted
kubectl ai "show unhealthy pods"
kubectl ai "scale deployment to 5"
```

### Key Specifications
| Spec | Purpose |
|------|---------|
| Cloud Architecture | Infrastructure design |
| Container Spec | Dockerfile requirements |
| K8s Manifests | Resource definitions |
| Helm values.yaml | Configuration management |
| ArgoCD Application | GitOps deployment |
| CI/CD Pipeline | Automation workflow |

### Security Checklist
- [ ] Non-root containers
- [ ] Read-only filesystem
- [ ] Resource limits defined
- [ ] Network policies configured
- [ ] Secrets externalized
- [ ] RBAC least privilege
- [ ] Pod security standards
- [ ] Image scanning enabled
