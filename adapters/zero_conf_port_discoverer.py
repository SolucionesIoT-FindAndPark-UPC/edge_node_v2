from zeroconf import Zeroconf, ServiceBrowser
from typing import List

from ports.port_discoverer import PortDiscoverer, DeviceInfo

hostnames = ["esp32server.local", "esp32server2.local"]

class ZeroconfDeviceDiscovery(PortDiscoverer):
    def discover_devices(self) -> List[DeviceInfo]:
        zeroconf = Zeroconf()
        devices = []

        class Listener:
            def add_service(self, zeroconf, type, name):
                info = zeroconf.get_service_info(type, name)
                if info:
                    devices.append(DeviceInfo(
                        name=name,
                        host=info.server,
                        ip=".".join(map(str, info.addresses[0]))
                    ))

        listener = Listener()
        browser = ServiceBrowser(zeroconf, "_http._tcp.local.", listener)
        import time; time.sleep(5)
        zeroconf.close()
        return devices

if __name__ == '__main__':
    zero = ZeroconfDeviceDiscovery()
    print(zero.discover_devices())