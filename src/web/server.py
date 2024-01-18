
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

T = TypeVar("T")

class Server(ABC, Generic[T]):
    @abstractmethod
    def emit(self, topic: str, message: str) -> bool:
        pass

    @abstractmethod
    def run(self) -> None:
        pass

    @abstractmethod
    def register_routes(self, request_mapping: str, method_view: T) -> None:
        pass