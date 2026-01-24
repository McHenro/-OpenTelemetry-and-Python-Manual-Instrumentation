import time
from celery import shared_task
from opentelemetry import trace
from .metrics import celery_task_duration, celery_error_counter

tracer = trace.get_tracer("orders.tasks")

@shared_task(bind=True)
def process_order_task(self, order_id: int):
    start_time = time.time()

    with tracer.start_as_current_span("celery.process_order") as span:
        try:
            span.set_attribute("order.id", order_id)

            time.sleep(2) # simulate work

            # Optional: simulate failure
            if order_id % 2 == 0:
                raise ValueError("Payment service failed")

            total = order_id * 100
            span.set_attribute("order.total", total)

        except Exception as e:
            # Increment error metric
            celery_error_counter.add(
                1,
                attributes={
                    "task.name": "process_order_task"
                }
            )

            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            raise

    duration_ms = (time.time() - start_time) * 1000
    celery_task_duration.record(
        duration_ms,
        attributes={"task.name": "process_order_task"}
    )

    return total