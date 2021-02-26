from dataclasses import dataclass

import boto3
from moto import mock_sqs

from auth.infrastructure.messaging.event.event import Event
from auth.infrastructure.messaging.event_publisher import EventPublisher


@dataclass
class EventMock(Event):
    event_id: str

    name = 'event_mock'


@mock_sqs
def test_publish():
    queue = 'mock-queue'
    sqs = boto3.resource('sqs')
    sqs.create_queue(QueueName=queue)
    event = EventMock(event_id='event-id')

    result = EventPublisher.publish(queue=queue, event=event)

    assert result
