import requests
from ports.servers_service import ServersService

class MainServer:
    @staticmethod
    def get():
        return 'http://127.0.0.1:8080/api/v1'

class MainServerService(ServersService):
    def get_all_users(self):
        url = f"{MainServer.get()}/users"
        try:
            response = requests.get(url, timeout=2)
            response.raise_for_status()
            print(f"{MainServer.get()}: {response.text}")
            users_response = response.json()
            return users_response
        except Exception as e:
            print(f"Could not reach {MainServer.get()}: {e}")

if __name__ == '__main__':
    server = MainServerService()
    print(server.get_all_users())