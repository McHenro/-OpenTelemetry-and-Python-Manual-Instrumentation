from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)


import time

provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer("my.tracer.name")


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
