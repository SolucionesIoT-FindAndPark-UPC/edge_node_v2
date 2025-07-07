import httpx

from ports.ip_recollector import IpRecollector


class IpifyIpRecollector(IpRecollector):
    def get_ip(self) -> str:
        response = httpx.get("https://api.ipify.org?format=json", timeout=5)
        response.raise_for_status()
        return response.json()["ip"]

if __name__ == "__main__":
    ip = IpifyIpRecollector()
    print(ip.get_ip())