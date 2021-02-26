import abc
import datetime
import uuid
from dataclasses import asdict, dataclass


@dataclass
class Event(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        pass

    def to_dict(self):
        return {
            'id': str(uuid.uuid4()),
            'name': self.name,
            'produced_at': datetime.datetime.now().isoformat(),
            'payload': asdict(self)
        }
