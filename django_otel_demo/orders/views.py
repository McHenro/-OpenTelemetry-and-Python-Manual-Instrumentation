from opentelemetry import trace
from .metrics import http_request_latency, http_error_counter
from django.http import JsonResponse
from .tasks import process_order_task
import time

tracer = trace.get_tracer("orders.views")

def create_order(request):
    start_time = time.time()

    with tracer.start_as_current_span("create_order_view") as span:
        try:
            order_id = 42
            span.set_attribute("order.id", order_id)
            span.set_attribute("http.method", request.method)

            # Enqueue async work instead of doing it inline
            process_order_task.delay(order_id)

            response = JsonResponse({
                "message": "Order processing started",
                "order_id": order_id
            })

        except Exception as e:
            # Increment error metric
            http_error_counter.add(
                1,
                attributes={
                    "http.method": request.method,
                    "http.route": "/orders/create",
                }
            )

            span.record_exception(e)
            span.set_status(trace.Status(trace.StatusCode.ERROR))
            return JsonResponse({"error": "Failed"}, status=500)

    # Record latency AFTER response logic
    duration_ms = (time.time() - start_time) * 1000
    http_request_latency.record(
        duration_ms,
        attributes={
            "http.method": request.method,
            "http.route": "/orders/create"
        }
    )

    return response