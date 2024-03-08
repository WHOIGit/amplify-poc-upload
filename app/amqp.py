import os

import json
import pika


async def amqp_publish(message):
    host = os.environ['RABBITMQ_HOST']
    user = os.environ['RABBITMQ_USER']
    password = os.environ['RABBITMQ_PASSWORD']

    exchange_name = os.environ['RABBITMQ_EXCHANGE']

    credentials = pika.PlainCredentials(user, password)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host, credentials=credentials)
    )
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    channel.basic_publish(exchange=exchange_name,
                          routing_key='',
                          body=json.dumps(message))

    connection.close()
