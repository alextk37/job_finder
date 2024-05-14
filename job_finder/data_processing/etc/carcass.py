from abc import ABC, abstractmethod


class Parser(ABC):

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def connection(self):
        pass

    @abstractmethod
    def save_data(self):
        pass
