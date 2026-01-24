# What This Project Demonstrates

I successfully demonstrated and implemented:

- Manual OpenTelemetry instrumentation (no auto-instrumentation)

- End-to-end distributed tracing across Django HTTP requests and Celery background tasks

- Parent–child span relationships between synchronous and asynchronous execution

- Trace context propagation from Django views to Celery workers

- Span attribute enrichment (business and HTTP metadata)

- Precise timing visibility for requests and background jobs

- Trace correlation across multiple services and processes

- Custom latency metrics using OpenTelemetry histograms:
  - HTTP request latency
  - Celery task execution duration

- Error metrics using counters for failed HTTP requests and Celery tasks

- Percentile-based performance analysis (e.g. p95 latency)

- OTLP exporters for traces and metrics

- SigNoz integration for:
  - Distributed trace visualization
  - Metrics dashboards
  - Latency and error-rate monitoring

- Production-style observability patterns, including alert-ready metrics and service metadata (service.name, environment, version)
