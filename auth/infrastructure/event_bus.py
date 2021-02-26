from pathlib import Path

from async_bus import EventBus
from autodiscover import AutoDiscover

bus = EventBus()

path = Path('auth/application/subscriber')
AutoDiscover(path)()
