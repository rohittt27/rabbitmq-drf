import json
import pika
import sys


def publish_to_rabbitmq(event_type, email_data):
    connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
            )
    channel = connection.channel()

    channel.queue_declare(queue='email_queue')


    message = {
        'event_type': event_type,
        'body': email_data,
    }

    message_json = json.dumps(message)

    channel.basic_publish(exchange='', routing_key='email_queue', body=message_json)
    print(f" [x] Sent {message}")
    connection.close()