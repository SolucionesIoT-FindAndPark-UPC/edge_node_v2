import httpx
import socket
from ports.ip_recollector import IpRecollector


class IpifyIpRecollector(IpRecollector):
    def get_ip(self) -> str:
        response = httpx.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json()["ip"]

    def get_local_ip(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't have to be reachable
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

if __name__ == "__main__":
    ip = IpifyIpRecollector()
    print(ip.get_ip())