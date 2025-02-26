from abc import ABC, abstractmethod

class IWriter(ABC):

    @abstractmethod
    def writing(self, data):
        pass