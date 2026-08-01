<div align="center">

# 🚚 LogiStream

### Real-Time Event-Driven Logistics Platform

A production-inspired backend project for asynchronous shipment processing using **FastAPI**, **Apache Kafka**, **PostgreSQL**, **Redis**, **Prometheus**, and **Grafana**.

*Event-Driven Architecture · Kafka Consumers · Cache-Aside · Analytics · Observability*

</div>

---

## Overview

LogiStream is a real-time logistics event-streaming platform built to demonstrate how a backend can move beyond synchronous CRUD operations into an event-driven architecture.

Shipment creation and status updates enter the system through a FastAPI REST API. Instead of writing those changes directly from the API layer, LogiStream publishes shipment events to an Apache Kafka topic. Independent consumers then process the same event stream for separate responsibilities:

- the **Shipment Consumer** persists shipment state and event history
- the **Analytics Consumer** maintains aggregated shipment metrics

PostgreSQL provides durable persistence, Redis implements a cache-aside read path for shipment lookups, and Prometheus + Grafana provide application observability.

> The project is intentionally focused on shipment processing rather than modelling an entire logistics business domain.

---

## Key Features

- Event-driven shipment processing through Apache Kafka
- FastAPI REST API for shipment creation, lookup, status updates, and analytics
- Independent Kafka consumer groups for shipment processing and analytics
- PostgreSQL persistence using SQLAlchemy
- Shipment event history for created and status-update events
- Redis cache-aside strategy for shipment reads
- Cache invalidation when shipment status changes
- Analytics aggregation for total, delivered, and in-transit shipments
- Alembic migrations for database schema management
- Prometheus metrics for API, Kafka, and Redis activity
- Grafana dashboard provisioning from code
- Docker Compose infrastructure for PostgreSQL, Kafka, Redis, Prometheus, and Grafana
- `uv`-based Python dependency management with a committed lockfile

---

## Architecture

```
                         ┌───────────────────┐
                         │      Client       │
                         └─────────┬─────────┘
                                   │ HTTP
                                   ▼
                         ┌───────────────────┐
                         │      FastAPI      │
                         │     REST API      │
                         └─────────┬─────────┘
                                   │
                              publish event
                                   │
                                   ▼
                         ┌───────────────────┐
                         │   Apache Kafka    │
                         │  shipment-events  │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Shipment Consumer│          │Analytics Consumer│
          └────────┬─────────┘          └────────┬─────────┘
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │    PostgreSQL    │          │ Analytics Table  │
          │ Shipments/Events │          │   PostgreSQL     │
          └────────┬─────────┘          └──────────────────┘
                    │
                    │ cache-aside reads
                    ▼
          ┌──────────────────┐
          │      Redis       │
          └──────────────────┘

          FastAPI /metrics
                    │
                    ▼
          ┌──────────────────┐
          │    Prometheus    │
          └────────┬─────────┘
                    ▼
          ┌──────────────────┐
          │     Grafana      │
          └──────────────────┘
```

### Event flow

**For a new shipment:**

```
POST /shipments
      │
      ▼
   FastAPI
      │
      ▼
SHIPMENT_CREATED event
      │
      ▼
Kafka: shipment-events
      ├──────────────→ Shipment Consumer  → shipments + shipment_events
      └──────────────→ Analytics Consumer → total_shipments
```

**For a status update:**

```
PATCH /shipments/{shipment_id}/status
      │
      ▼
   FastAPI
      │
      ▼
SHIPMENT_STATUS_UPDATED event
      │
      ▼
Kafka
      ├──────────────→ Shipment Consumer  → update shipment + invalidate Redis
      └──────────────→ Analytics Consumer → update status analytics
```

---

## Tech Stack

| Layer          | Technology         | Role                                              |
|----------------|--------------------|----------------------------------------------------|
| API            | FastAPI            | REST endpoints and dependency injection            |
| Language       | Python 3.10+       | Application implementation                         |
| Messaging      | Apache Kafka       | Event transport and asynchronous processing        |
| Database       | PostgreSQL 17      | Shipment, event-history, and analytics persistence |
| ORM            | SQLAlchemy 2       | Database models and data access                    |
| Migrations     | Alembic            | Schema migrations                                   |
| Cache          | Redis 8            | Cache-aside shipment lookup                         |
| Metrics        | Prometheus Client  | Application metrics                                 |
| Monitoring     | Prometheus         | Metrics scraping and time-series storage            |
| Visualization  | Grafana            | Provisioned operations dashboard                    |
| Infrastructure | Docker Compose     | Local infrastructure orchestration                  |

---

## Engineering Concepts Demonstrated

| Concept                    | LogiStream implementation                                                          |
|-----------------------------|--------------------------------------------------------------------------------------|
| Event-Driven Architecture   | API publishes shipment events to Kafka instead of synchronously performing all downstream work |
| Producer–Consumer Pattern   | Kafka producer with independent shipment and analytics consumers                    |
| Consumer Groups             | `shipment-consumer` and `analytics-consumer` process the same topic independently   |
| Repository Pattern          | Database operations are isolated in repository classes                              |
| Service Layer               | Shipment and analytics business logic live outside API routes                       |
| Dependency Injection        | FastAPI `Depends(get_db)` provides database sessions                                |
| Cache-Aside                 | Shipment reads check Redis first, then PostgreSQL on a miss                         |
| Cache Invalidation          | Shipment cache entry is deleted after a status update                               |
| Event History                | Shipment events are persisted separately from current shipment state               |
| Observability                | Prometheus counters are exposed through `/metrics` and visualized in Grafana       |

---

## Project Structure

```
logistream/
├── app/
│   ├── api/
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── cache/
│   │   └── redis_client.py
│   ├── config/
│   │   └── settings.py
│   ├── consumers/
│   │   ├── analytics_consumer.py
│   │   └── shipment_consumer.py
│   ├── database/
│   │   ├── base.py
│   │   └── session.py
│   ├── models/
│   │   ├── analytics.py
│   │   ├── shipment.py
│   │   └── shipment_event.py
│   ├── producers/
│   │   └── kafka_producer.py
│   ├── repositories/
│   │   ├── analytics_repository.py
│   │   ├── shipment_event_repository.py
│   │   └── shipment_repository.py
│   ├── services/
│   │   ├── analytics_service.py
│   │   └── shipment_service.py
│   ├── main.py
│   └── metrics.py
├── grafana/
│   ├── dashboards/
│   └── provisioning/
│       ├── dashboards/
│       └── datasources/
├── migrations/
├── screenshots/
├── scripts/
├── docker-compose.yml
├── prometheus.yml
├── alembic.ini
├── pyproject.toml
├── uv.lock
├── .python-version
├── .env.example
└── README.md
```

---

## API Endpoints

| Method | Endpoint                            | Purpose                                            |
|--------|--------------------------------------|-----------------------------------------------------|
| GET    | `/`                                  | Application status/welcome endpoint                 |
| POST   | `/shipments`                         | Publish a `SHIPMENT_CREATED` event                  |
| GET    | `/shipments/{shipment_id}`           | Retrieve a shipment using Redis/PostgreSQL cache-aside lookup |
| PATCH  | `/shipments/{shipment_id}/status`    | Publish a shipment status-update event               |
| GET    | `/analytics`                         | Retrieve aggregated shipment analytics               |

### Create a shipment

```json
{
  "shipment_id": "shipment-1001",
  "origin": "Delhi",
  "destination": "Mumbai"
}
```

The API publishes a `SHIPMENT_CREATED` event and immediately acknowledges publication:

```json
{
  "message": "Shipment event published successfully"
}
```

### Update shipment status

```
PATCH /shipments/shipment-1001/status
```

```json
{
  "status": "IN_TRANSIT"
}
```

---

## Redis Caching Strategy

LogiStream uses the cache-aside pattern for shipment reads.

```
GET /shipments/{id}
        │
        ▼
      Redis
      /   \
   HIT     MISS
    │       │
    │       ▼
    │   PostgreSQL
    │       │
    │       ▼
    │   populate cache
    │       │
    └───────┴──────→ response
```

When a shipment is requested:

1. The service checks `shipment:{shipment_id}` in Redis.
2. On a cache **hit**, the cached shipment is returned.
3. On a cache **miss**, PostgreSQL is queried.
4. The retrieved shipment is serialized into Redis for subsequent reads.
5. When a shipment status changes, its Redis key is deleted so stale state is not served.

The application also increments Prometheus counters for cache hits and misses.

---

## Analytics Consumer

The analytics consumer belongs to a separate Kafka consumer group: `analytics-consumer`.

It consumes the same `shipment-events` topic independently from the shipment consumer.

Current aggregated metrics include:

- `total_shipments`
- `delivered_shipments`
- `in_transit_shipments`

This demonstrates how a single event stream can support multiple downstream use cases without coupling those responsibilities into the API.

---

## Observability

LogiStream exposes Prometheus metrics from FastAPI at:

```
http://localhost:8000/metrics
```

### Application metrics

| Metric                          | Meaning                                              |
|----------------------------------|-------------------------------------------------------|
| `api_requests_total`             | API requests counted by instrumented LogiStream routes |
| `kafka_messages_processed_total` | Kafka events processed by the shipment consumer        |
| `cache_hits_total`               | Shipment lookups served from Redis                     |
| `cache_misses_total`             | Shipment lookups that missed Redis                     |

Prometheus is configured to scrape the FastAPI metrics endpoint every 5 seconds.

### Grafana

Grafana is provisioned from files in the repository:

```
grafana/
├── dashboards/
└── provisioning/
    ├── dashboards/
    └── datasources/
```

The Prometheus datasource is created automatically and the LogiStream dashboard can be loaded without manually rebuilding the panels.

> Prometheus application counters live in the application process. Restarting FastAPI resets the current exported counter values; Prometheus functions such as `rate()` are designed to handle counter resets when historical samples are available.

---

## Getting Started

### Prerequisites

Install:

- Docker + Docker Compose
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

### 1. Clone the repository

```bash
git clone https://github.com/<your-github-username>/logistream.git
cd logistream
```

### 2. Install Python dependencies

The repository uses `pyproject.toml` and `uv.lock`.

```bash
uv sync
```

### 3. Configure environment variables

Create `.env` in the project root. The application expects the following settings:

```env
APP_NAME=LogiStream
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=postgresql+psycopg2://logistream:logistream@localhost:5433/logistream
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_URL=redis://localhost:6379/0
```

> `.env` should remain local and must not be committed. Use `.env.example` as the public template.

### 4. Start infrastructure

```bash
docker compose up -d
```

This starts:

- PostgreSQL — host port `5433`
- Kafka — host port `9092`
- Redis — host port `6379`
- Prometheus — host port `9090`
- Grafana — host port `3000`

Verify:

```bash
docker compose ps
```

### 5. Apply database migrations

```bash
uv run alembic upgrade head
```

### 6. Start FastAPI

```bash
uv run uvicorn app.main:app --reload
```

- FastAPI: [http://localhost:8000](http://localhost:8000)
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

### 7. Start the shipment consumer

Open another terminal:

```bash
uv run python -m app.consumers.shipment_consumer
```

### 8. Start the analytics consumer

Open another terminal:

```bash
uv run python -m app.consumers.analytics_consumer
```

At this point the complete event-processing pipeline is running.

---

## Local Services

| Service             | Address                              |
|----------------------|---------------------------------------|
| FastAPI              | http://localhost:8000                |
| Swagger UI            | http://localhost:8000/docs           |
| FastAPI Metrics       | http://localhost:8000/metrics        |
| Prometheus            | http://localhost:9090                |
| Prometheus Targets    | http://localhost:9090/targets        |
| Grafana                | http://localhost:3000                |
| PostgreSQL             | localhost:5433                        |
| Kafka                   | localhost:9092                        |
| Redis                    | localhost:6379                        |

> For Prometheus to collect application metrics, FastAPI must be running and the `logistream` target on the Prometheus Targets page should report `UP`.

---

## Running the Event Flow

With Docker, FastAPI, and both consumers running:

1. Open Swagger at [http://localhost:8000/docs](http://localhost:8000/docs).
2. Call `POST /shipments` with a new shipment ID.
   - The API publishes the event to `shipment-events`.
   - The shipment consumer persists the shipment and its event.
   - The analytics consumer updates aggregate analytics.
3. Call `GET /shipments/{shipment_id}`:
   - first read → Redis miss → PostgreSQL lookup → cache populated
   - subsequent read → Redis hit
4. Update the shipment through `PATCH /shipments/{shipment_id}/status`.
   - The shipment consumer updates PostgreSQL and invalidates the cached shipment.
5. Observe API/cache/Kafka metrics in Prometheus and Grafana.

---

## Why Kafka?

The API does not need to synchronously execute every downstream responsibility.

Kafka provides a durable event stream that allows different consumers to react independently:

```
                    shipment-events
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      shipment-consumer         analytics-consumer
             │                         │
      shipment state             aggregate metrics
```

This separation makes it possible to add future consumers without embedding their logic into the API request path.

## Why Redis?

Shipment lookups can be read repeatedly while shipment state changes less frequently.

The cache-aside strategy allows Redis to serve repeated reads while PostgreSQL remains the source of truth. Status updates invalidate the relevant cache entry so the next read repopulates it from current database state.

---

## Screenshots

**Grafana Operations Dashboard**

Additional screenshots are available in the `screenshots` directory.

---

## Future Scope

The current version deliberately keeps the shipment domain small. Potential future improvements include:

- shipment simulation/sample-data generation
- business-focused Grafana analytics
- shipment status distribution charts
- geographical origin/destination visualization
- consumer lag monitoring
- API latency histograms
- automated alerting
- retry/dead-letter handling for failed events
- stronger producer delivery guarantees
- authentication and authorization
- CI/CD
- containerized FastAPI/consumer services
- Kubernetes deployment

These are intentionally left outside the current v1 scope rather than increasing domain complexity unnecessarily.

---

## What This Project Demonstrates

LogiStream was built as a hands-on exploration of how components commonly used in modern data/backend systems fit together:

```
REST API
   +
Event Streaming
   +
Persistent Storage
   +
Caching
   +
Independent Consumers
   +
Operational Analytics
   +
Observability
   +
Containerized Infrastructure
```

The primary goal is not simply shipment CRUD — it is understanding the flow of data through an asynchronous, observable system.

<div align="center">

Built with **FastAPI** · **Kafka** · **PostgreSQL** · **Redis** · **Prometheus** · **Grafana**

</div>