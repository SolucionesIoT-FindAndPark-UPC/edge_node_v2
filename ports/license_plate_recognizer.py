from abc import ABC, abstractmethod


class LicensePlateRecognizer(ABC):
    @abstractmethod
    def recognize(self, image):
        pass