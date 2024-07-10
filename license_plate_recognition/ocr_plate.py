import pytesseract
import cv2

def ocr_license_plate(image_path):
    license_plate = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    license_plate_text = pytesseract.image_to_string(license_plate, config='--psm 8')
    return license_plate_text