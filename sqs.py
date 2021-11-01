from boto3 import resource
from functools import lru_cache
from json import dumps
from os import getenv


@lru_cache()
def get_sqs_resource():
    return resource('sqs')


def send_message(message, alert):
    aws_resource = get_sqs_resource()

    queue = aws_resource.get_queue_by_name(QueueName=alert.get("QueueName"))
    body = dumps(message)
    if alert.get("Fifo"):
        queue.send_message(MessageBody=body, MessageGroupId=alert.get('GroupId'))
    else:
        queue.send_message(MessageBody=body)
