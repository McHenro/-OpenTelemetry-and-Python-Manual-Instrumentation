from opentelemetry import trace
from django.http import JsonResponse
from .tasks import process_order_task

tracer = trace.get_tracer("orders.views")

def create_order(request):
    with tracer.start_as_current_span("create_order_view") as span:
        order_id = 42
        span.set_attribute("order.id", order_id)
        span.set_attribute("http.method", request.method)

        # Enqueue async work instead of doing it inline
        process_order_task.delay(order_id)

        return JsonResponse({
            "message": "Order processing started",
            "order_id": order_id
        })

