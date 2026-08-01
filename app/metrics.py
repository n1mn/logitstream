from prometheus_client import Counter

api_requests_total = Counter(
    "api_requests_total",
    "Total number of API requests",
)

kafka_messages_processed = Counter(
    "kafka_messages_processed_total",
    "Total number of Kafka messages processed",
)
cache_hits_total = Counter(
    "cache_hits_total",
    "Total Redis cache hits",
)

cache_misses_total = Counter(
    "cache_misses_total",
    "Total Redis cache misses",
)