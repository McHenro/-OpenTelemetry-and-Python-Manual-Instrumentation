import time
from celery import shared_task
from opentelemetry import trace
from .metrics import celery_task_duration

tracer = trace.get_tracer("orders.tasks")

@shared_task
def process_order_task(order_id: int):
    start_time = time.time()

    with tracer.start_as_current_span("celery.process_order") as span:
        span.set_attribute("order.id", order_id)

        time.sleep(2)  # simulate work

        total = order_id * 100
        span.set_attribute("order.total", total)

    duration_ms = (time.time() - start_time) * 1000
    celery_task_duration.record(
        duration_ms,
        attributes={
            "task.name": "process_order_task"
        }
    )

    return total