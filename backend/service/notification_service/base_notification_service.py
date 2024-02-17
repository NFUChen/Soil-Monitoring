from abc import ABC, abstractmethod


class BaseNotificationService(ABC):
    @abstractmethod
    def push_notification(self, topic: str,message: str) -> bool:
        raise NotImplementedError()