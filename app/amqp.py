import os

import json
import aio_pika


async def amqp_publish(message):
    host = os.environ['RABBITMQ_HOST']
    user = os.environ['RABBITMQ_USER']
    password = os.environ['RABBITMQ_PASSWORD']

    exchange_name = os.environ['RABBITMQ_EXCHANGE']

    connection = await aio_pika.connect_robust(
        f"amqp://{user}:{password}@{host}/"
    )
    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(exchange_name, aio_pika.ExchangeType.FANOUT)

        await exchange.publish(
            aio_pika.Message(body=json.dumps(message).encode()),
            routing_key=''
        )