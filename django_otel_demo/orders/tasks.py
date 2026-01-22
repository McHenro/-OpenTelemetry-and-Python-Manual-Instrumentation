import time
from celery import shared_task
from opentelemetry import trace

tracer = trace.get_tracer("orders.tasks")

@shared_task
def process_order_task(order_id: int):
    with tracer.start_as_current_span("celery.process_order") as span:
        span.set_attribute("order.id", order_id)

        time.sleep(2)  # simulate work

        total = order_id * 100
        span.set_attribute("order.total", total)

        return total
