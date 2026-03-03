import asyncio
import json
import os

import aio_pika


QUEUE_NAME = "thunderbird.domain.events"
DLQ_NAME = "thunderbird.domain.events.dlq"
MAX_RETRIES = 5


async def process_message(payload: dict) -> None:
    # Placeholder: invoke moderation/notification/content processing routines.
    print(f"processing event: {payload.get('event_type', 'unknown')}")


async def run_worker() -> None:
    rabbit_url = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")
    connection = await aio_pika.connect_robust(rabbit_url)

    async with connection:
        channel = await connection.channel()
        await channel.set_qos(prefetch_count=10)

        exchange = await channel.declare_exchange("thunderbird", aio_pika.ExchangeType.TOPIC, durable=True)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        dlq = await channel.declare_queue(DLQ_NAME, durable=True)

        await queue.bind(exchange, routing_key="domain.*")
        await dlq.bind(exchange, routing_key="domain.dlq")

        async with queue.iterator() as iterator:
            async for message in iterator:
                async with message.process(ignore_processed=True):
                    headers = message.headers or {}
                    retry_count = int(headers.get("x-retry", 0))

                    try:
                        payload = json.loads(message.body.decode("utf-8"))
                        await process_message(payload)
                        await message.ack()
                    except Exception:
                        if retry_count >= MAX_RETRIES:
                            await exchange.publish(
                                aio_pika.Message(
                                    body=message.body,
                                    headers={"x-retry": retry_count},
                                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                                ),
                                routing_key="domain.dlq",
                            )
                            await message.ack()
                        else:
                            await exchange.publish(
                                aio_pika.Message(
                                    body=message.body,
                                    headers={"x-retry": retry_count + 1},
                                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                                ),
                                routing_key="domain.retry",
                            )
                            await message.ack()


if __name__ == "__main__":
    asyncio.run(run_worker())
