from os import name
import requests

from ports.servers_service import ServersService


class Esp32Servers:
    @staticmethod
    def get_servo_controller():
        return 'esp32server.local'
    @staticmethod
    def get_camera1():
        return 'esp32cam-server.local'
    @staticmethod
    def get_camera2():
        return ''


class Esp32ServersService(ServersService):
    def open_entry(self):
        url = f"http://{Esp32Servers.get_servo_controller()}:8050/open"
        try:
            response = requests.get(url, timeout=2)
            print(f"{Esp32Servers.get_servo_controller()}: {response.text}")
        except Exception as e:
            print(f"Could not reach {Esp32Servers.get_servo_controller()}: {e}")
    def close_entry(self):
        url = f"http://{Esp32Servers.get_servo_controller()}:8050/close"
        try:
            response = requests.get(url, timeout=2)
            print(f"{Esp32Servers.get_servo_controller()}: {response.text}")
        except Exception as e:
            print(f"Could not reach {Esp32Servers.get_servo_controller()}: {e}")
    def open_exit(self):
        url = f"http://{Esp32Servers.get_servo_controller()}:8050/open_two"
        try:
            response = requests.get(url, timeout=2)
            print(f"{Esp32Servers.get_servo_controller()}: {response.text}")
        except Exception as e:
            print(f"Could not reach {Esp32Servers.get_servo_controller()}: {e}")
    def close_exit(self):
        url = f"http://{Esp32Servers.get_servo_controller()}:8050/close_two"
        try:
            response = requests.get(url, timeout=2)
            print(f"{Esp32Servers.get_servo_controller()}: {response.text}")
        except Exception as e:
            print(f"Could not reach {Esp32Servers.get_servo_controller()}: {e}")
    def get_image(self):
        url = f"http://{Esp32Servers.get_camera1()}:80/capture"
        try:
            response = requests.get(url, timeout=30)
            print(f"{Esp32Servers.get_servo_controller()}: {response.text}")
        except Exception as e:
            print(f"Could not reach {Esp32Servers.get_servo_controller()}: {e}")

if __name__ == "__main__":
    servers_service = Esp32ServersService()
    servers_service.get_image()
