from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

import time


# ----------------------------
# Resource (Service Identity)
# ----------------------------
resource = Resource.create({
    SERVICE_NAME: "python-otel-demo",
    "service.version": "0.1.0",
    "deployment.environment": "local",
})

# ----------------------------
# Tracer Provider Setup
# ----------------------------
provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")

# ----------------------------
# Application Logic
# ----------------------------
def process_order(order_id: int):
    with tracer.start_as_current_span("process_order") as span:
        span.set_attribute("order.id", order_id)

        # Simulate work
        time.sleep(1)

        total = calculate_price(order_id)
        span.set_attribute("order.total", total)

        return total

def calculate_price(order_id: int):
    with tracer.start_as_current_span("calculate_price") as span:
        span.set_attribute("order.id", order_id)

        time.sleep(0.5)
        return order_id * 100

if __name__ == "__main__":
    result = (process_order(3))
    print(result)