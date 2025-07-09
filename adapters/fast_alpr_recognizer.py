from ports.license_plate_recognizer import LicensePlateRecognizer
from fast_alpr import ALPR


class FastAlprRecognizer(LicensePlateRecognizer):
    def __init__(self):
        print("[INFO] Cargando modelo fast-alpr desde archivos locales...")
        self.alpr = ALPR(
            detector_model="yolo-v9-t-384-license-plate-end2end",
            ocr_model="global-plates-mobile-vit-v2-model"
        )
    def recognize(self, image: str) -> str:
        results = self.alpr.predict(image)
        if results:
            return results[0].ocr.text
        return ""

if __name__ == "__main__":
    fast = FastAlprRecognizer()