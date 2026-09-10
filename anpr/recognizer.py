import cv2
import easyocr
import numpy as np
from anpr.validator import validate_plate
from PIL import Image


class PlateEngine:
    def __init__(self, gpu = False):
        self.reader = easyocr.Reader(["en"], gpu=gpu)

    def preprocess(self, image: np.ndarray):
        #Enhances contrast and reduces noise for OCR.
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Bilateral filter removes noise while keeping edges sharp
        filtered = cv2.bilateralFilter(gray, 11, 17, 17)
        return filtered

    def process_image(self, image_path, min_confidence = 0.30):
        try:
            pil_img = Image.open(image_path).convert("RGB")
            # Convert PIL RGB array to OpenCV BGR format
            img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        except Exception as e:
            raise FileNotFoundError(f"Failed to read image at {image_path}: {e}")

        processed = self.preprocess(img)
        detections = self.reader.readtext(processed)
        results = []

        for bbox, raw_text, conf in detections:
            if conf < min_confidence:
                continue

            is_valid, formatted_plate = validate_plate(raw_text)
            if is_valid:
                results.append({
                    "plate": formatted_plate,
                    "confidence": round(float(conf), 3),
                    "box": [list(map(int, pt)) for pt in bbox]
                })

        return results