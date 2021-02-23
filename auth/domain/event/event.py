import abc


class Event(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self):
        pass

    def to_dict(self):
        return self.__dict__
