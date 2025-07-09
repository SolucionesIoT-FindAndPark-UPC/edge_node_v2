from abc import abstractmethod, ABC
from typing import List


class DeviceInfo:
    def __init__(self, name: str, host: str, ip: str):
        self.name = name
        self.host = host
        self.ip = ip

class PortDiscoverer(ABC):
    @abstractmethod
    def discover_devices(self) -> List[DeviceInfo]:
        pass