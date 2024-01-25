from abc import ABC, abstractmethod


class AbstractConsole(ABC):

    @abstractmethod
    def alert(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def info(self, text: str) -> None:
        raise NotImplementedError

    @abstractmethod
    def warn(self, text: str) -> None:
        raise NotImplementedError



