import json

import boto3


class EventPublisher:

    @staticmethod
    def publish(queue, event):
        sqs = boto3.resource('sqs')
        sqs_queue = sqs.get_queue_by_name(QueueName=queue)

        response = sqs_queue.send_message(MessageBody=json.dumps(event.to_dict()))

        return response.get('MessageId')
