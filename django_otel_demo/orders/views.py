from opentelemetry import trace
from django.http import JsonResponse
import time

tracer = trace.get_tracer("orders.views")


def create_order(request):
    with tracer.start_as_current_span("create_order_view") as span:
        order_id = 42
        span.set_attribute("order.id", order_id)
        span.set_attribute("http.method", request.method)

        time.sleep(0.3)

        total = calculate_price(order_id)
        span.set_attribute("order.total", total)

        return JsonResponse({
            "order_id": order_id,
            "total": total
        })


def calculate_price(order_id: int):
    with tracer.start_as_current_span("calculate_price") as span:
        span.set_attribute("order.id", order_id)
        time.sleep(0.2)
        return order_id * 100

