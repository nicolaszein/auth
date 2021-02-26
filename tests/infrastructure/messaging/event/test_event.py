from dataclasses import dataclass

from auth.infrastructure.messaging.event.event import Event


@dataclass
class EventMock(Event):
    event_id: str

    name = 'event_mock'


def test_to_dict():
    event = EventMock(event_id='event-id')

    result = event.to_dict()

    assert result['id']
    assert result['name'] == 'event_mock'
    assert result['produced_at']
    assert result['payload'] == {'event_id': 'event-id'}
