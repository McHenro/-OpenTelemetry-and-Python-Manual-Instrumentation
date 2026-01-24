# orders/metrics.py
from opentelemetry import metrics

# Get a named meter (logical grouping)
meter = metrics.get_meter("orders.metrics")

# HTTP request latency histogram
http_request_latency = meter.create_histogram(
    name="http.request.duration",
    unit="ms",
    description="HTTP request latency"
)

# Celery task duration histogram
celery_task_duration = meter.create_histogram(
    name="celery.task.duration",
    unit="ms",
    description="Celery task execution duration"
)
