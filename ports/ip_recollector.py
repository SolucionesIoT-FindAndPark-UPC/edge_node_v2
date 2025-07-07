from abc import ABC, abstractmethod


class IpRecollector(ABC):
    @abstractmethod
    def get_ip(self) -> str:
        pass