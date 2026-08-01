::: {align="center"}

🚚 LogiStream

Real-Time Event-Driven Logistics Platform

A production-inspired backend project for asynchronous shipmentprocessing using FastAPI, Apache Kafka, PostgreSQL, Redis, Prometheus,and Grafana.





Event-Driven Architecture · Kafka Consumers · Cache-Aside · Analytics· Observability:::

Overview

LogiStream is a real-time logistics event-streaming platform builtto demonstrate how a backend can move beyond synchronous CRUD operationsinto an event-driven architecture.

Shipment creation and status updates enter the system through a FastAPIREST API. Instead of writing those changes directly from the API layer,LogiStream publishes shipment events to an Apache Kafka topic.Independent consumers then process the same event stream for separateresponsibilities:

the Shipment Consumer persists shipment state and event history;

the Analytics Consumer maintains aggregated shipment metrics.

PostgreSQL provides durable persistence, Redis implements a cache-asideread path for shipment lookups, and Prometheus + Grafana provideapplication observability.

The project is intentionally focused on shipment processing rather thanmodelling an entire logistics business domain.

Key Features

Event-driven shipment processing through Apache Kafka

FastAPI REST API for shipment creation, lookup, status updates,and analytics

Independent Kafka consumer groups for shipment processing andanalytics

PostgreSQL persistence using SQLAlchemy

Shipment event history for created and status-update events

Redis cache-aside strategy for shipment reads

Cache invalidation when shipment status changes

Analytics aggregation for total, delivered, and in-transitshipments

Alembic migrations for database schema management

Prometheus metrics for API, Kafka, and Redis activity

Grafana dashboard provisioning from code

Docker Compose infrastructure for PostgreSQL, Kafka, Redis,Prometheus, and Grafana

uv-based Python dependency management with a committed lockfile

Architecture

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
                         │ shipment-events   │
                         └─────────┬─────────┘
                                   │
                    ┌──────────────┴──────────────┐
                    │                             │
                    ▼                             ▼
          ┌──────────────────┐          ┌──────────────────┐
          │ Shipment Consumer│          │Analytics Consumer│
          └────────┬─────────┘          └────────┬─────────┘
                   │                              │
                   ▼                              ▼
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

Event flow

For a new shipment:

POST /shipments
      ↓
FastAPI
      ↓
SHIPMENT_CREATED event
      ↓
Kafka: shipment-events
      ├──────────────→ Shipment Consumer → shipments + shipment_events
      └──────────────→ Analytics Consumer → total_shipments

For a status update:

PATCH /shipments/{shipment_id}/status
      ↓
FastAPI
      ↓
SHIPMENT_STATUS_UPDATED event
      ↓
Kafka
      ├──────────────→ Shipment Consumer → update shipment + invalidate Redis
      └──────────────→ Analytics Consumer → update status analytics

Tech Stack

Layer                   Technology              Role

API                     FastAPI                 REST endpoints anddependency injection

Language                Python 3.10+            Applicationimplementation

Messaging               Apache Kafka            Event transport andasynchronous processing

Database                PostgreSQL 17           Shipment,event-history, andanalytics persistence

ORM                     SQLAlchemy 2            Database models anddata access

Migrations              Alembic                 Schema migrations

Cache                   Redis 8                 Cache-aside shipmentlookup

Metrics                 Prometheus Client       Application metrics

Monitoring              Prometheus              Metrics scraping andtime-series storage

Visualization           Grafana                 Provisioned operationsdashboard

Infrastructure          Docker Compose          Local infrastructureorchestration

Engineering Concepts Demonstrated

Concept                             LogiStream implementation

Event-Driven Architecture           API publishes shipment events toKafka instead of synchronouslyperforming all downstream work

Producer--Consumer Pattern          Kafka producer with independentshipment and analytics consumers

Consumer Groups                     shipment-consumer andanalytics-consumer process thesame topic independently

Repository Pattern                  Database operations are isolated inrepository classes

Service Layer                       Shipment and analytics businesslogic live outside API routes

Dependency Injection                FastAPI Depends(get_db) providesdatabase sessions

Cache-Aside                         Shipment reads check Redis first,then PostgreSQL on a miss

Cache Invalidation                  Shipment cache entry is deletedafter a status update

Event History                       Shipment events are persistedseparately from current shipmentstate

Observability                       Prometheus counters are exposedthrough /metrics and visualizedin Grafana

Project Structure

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

API Endpoints

Method                  Endpoint                            Purpose

GET                   /                                 Applicationstatus/welcome endpoint

POST                  /shipments                        Publish aSHIPMENT_CREATEDevent

GET                   /shipments/{shipment_id}          Retrieve a shipmentusing Redis/PostgreSQLcache-aside lookup

PATCH                 /shipments/{shipment_id}/status   Publish a shipmentstatus-update event

GET                   /analytics                        Retrieve aggregatedshipment analytics

Create a shipment

{
  "shipment_id": "shipment-1001",
  "origin": "Delhi",
  "destination": "Mumbai"
}

The API publishes a SHIPMENT_CREATED event and immediatelyacknowledges publication:

{
  "message": "Shipment event published successfully"
}

Update shipment status

{
  "status": "IN_TRANSIT"
}

Example endpoint:

PATCH /shipments/shipment-1001/status

Redis Caching Strategy

LogiStream uses the cache-aside pattern for shipment reads.

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

When a shipment is requested:

The service checks shipment:{shipment_id} in Redis.

On a cache hit, the cached shipment is returned.

On a cache miss, PostgreSQL is queried.

The retrieved shipment is serialized into Redis for subsequentreads.

When a shipment status changes, its Redis key is deleted so stalestate is not served.

The application also increments Prometheus counters for cache hits andmisses.

Analytics Consumer

The analytics consumer belongs to a separate Kafka consumer group:

analytics-consumer

It consumes the same shipment-events topic independently from theshipment consumer.

Current aggregated metrics include:

total_shipments

delivered_shipments

in_transit_shipments

This demonstrates how a single event stream can support multipledownstream use cases without coupling those responsibilities into theAPI.

Observability

LogiStream exposes Prometheus metrics from FastAPI at:

http://localhost:8000/metrics

Application metrics

Metric                              Meaning

api_requests_total                API requests counted byinstrumented LogiStream routes

kafka_messages_processed_total    Kafka events processed by theshipment consumer

cache_hits_total                  Shipment lookups served from Redis

cache_misses_total                Shipment lookups that missed Redis

Prometheus is configured to scrape the FastAPI metrics endpoint every5 seconds.

Grafana

Grafana is provisioned from files in the repository:

grafana/
├── dashboards/
└── provisioning/
    ├── dashboards/
    └── datasources/

The Prometheus datasource is created automatically and the LogiStreamdashboard can be loaded without manually rebuilding the panels.

Prometheus application counters live in the application process.Restarting FastAPI resets the current exported counter values;Prometheus functions such as rate() are designed to handle counterresets when historical samples are available.

Getting Started

Prerequisites

Install:

Docker + Docker Compose

Python 3.10+

uv

1. Clone the repository

git clone https://github.com/<your-github-username>/logistream.git
cd logistream

2. Install Python dependencies

The repository uses pyproject.toml and uv.lock.

uv sync

3. Configure environment variables

Create .env in the project root.

The application expects the following settings:

APP_NAME=LogiStream
APP_VERSION=0.1.0
ENVIRONMENT=development
DEBUG=true

DATABASE_URL=postgresql+psycopg2://logistream:logistream@localhost:5433/logistream
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
REDIS_URL=redis://localhost:6379/0

.env should remain local and must not be committed. Use.env.example as the public template.

4. Start infrastructure

docker compose up -d

This starts:

PostgreSQL --- host port 5433

Kafka --- host port 9092

Redis --- host port 6379

Prometheus --- host port 9090

Grafana --- host port 3000

Verify:

docker compose ps

5. Apply database migrations

uv run alembic upgrade head

6. Start FastAPI

uv run uvicorn app.main:app --reload

FastAPI:

http://localhost:8000

Swagger UI:

http://localhost:8000/docs

7. Start the shipment consumer

Open another terminal:

uv run python -m app.consumers.shipment_consumer

8. Start the analytics consumer

Open another terminal:

uv run python -m app.consumers.analytics_consumer

At this point the complete event-processing pipeline is running.

Local Services

Service              Address

FastAPI              http://localhost:8000Swagger UI           http://localhost:8000/docsFastAPI Metrics      http://localhost:8000/metricsPrometheus           http://localhost:9090Prometheus Targets   http://localhost:9090/targetsGrafana              http://localhost:3000PostgreSQL           localhost:5433Kafka                localhost:9092Redis                localhost:6379

For Prometheus to collect application metrics, FastAPI must be runningand the logistream target on the Prometheus Targets page should reportUP.

Running the Event Flow

With Docker, FastAPI, and both consumers running:

Open Swagger at http://localhost:8000/docs.

Call POST /shipments with a new shipment ID.

The API publishes the event to shipment-events.

The shipment consumer persists the shipment and its event.

The analytics consumer updates aggregate analytics.

Call GET /shipments/{shipment_id}:

first read → Redis miss → PostgreSQL lookup → cache populated;

subsequent read → Redis hit.

Update the shipment through PATCH /shipments/{shipment_id}/status.

The shipment consumer updates PostgreSQL and invalidates the cachedshipment.

Observe API/cache/Kafka metrics in Prometheus and Grafana.

Why Kafka?

The API does not need to synchronously execute every downstreamresponsibility.

Kafka provides a durable event stream that allows different consumers toreact independently:

                    shipment-events
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
      shipment-consumer         analytics-consumer
             │                         │
      shipment state             aggregate metrics

This separation makes it possible to add future consumers withoutembedding their logic into the API request path.

Why Redis?

Shipment lookups can be read repeatedly while shipment state changesless frequently.

The cache-aside strategy allows Redis to serve repeated reads whilePostgreSQL remains the source of truth. Status updates invalidate therelevant cache entry so the next read repopulates it from currentdatabase state.

Screenshots

Grafana Operations Dashboard



Additional screenshots are available in thescreenshots directory.

Future Scope

The current version deliberately keeps the shipment domain small.Potential future improvements include:

shipment simulation/sample-data generation

business-focused Grafana analytics

shipment status distribution charts

geographical origin/destination visualization

consumer lag monitoring

API latency histograms

automated alerting

retry/dead-letter handling for failed events

stronger producer delivery guarantees

authentication and authorization

CI/CD

containerized FastAPI/consumer services

Kubernetes deployment

These are intentionally left outside the current v1 scope rather thanincreasing domain complexity unnecessarily.

What This Project Demonstrates

LogiStream was built as a hands-on exploration of how componentscommonly used in modern data/backend systems fit together:

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

The primary goal is not simply shipment CRUD---it is understanding theflow of data through an asynchronous, observable system.

::: {align="center"}

Built with FastAPI · Kafka · PostgreSQL · Redis · Prometheus · Grafana

:::