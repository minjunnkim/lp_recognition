import cv2
from .utils import read_license_plate

def ocr_license_plate(image_path):
    license_plate_crop = cv2.imread(image_path)
    license_plate_text, score = read_license_plate(license_plate_crop)
    return license_plate_text

# Path to the detected license plate image
plate_image_path = 'images/license_plate.jpg'

# Performing OCR on the license plate image
license_plate_text = ocr_license_plate(plate_image_path)
print(license_plate_text)