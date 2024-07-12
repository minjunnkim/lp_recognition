import easyocr
import re
import cv2

# Initialize the OCR reader
reader = easyocr.Reader(['en'], gpu=False)

def is_valid_license_plate(text):
    # Check if the text contains only letters and digits
    return bool(re.match("^[A-Z0-9]*$", text))

def read_license_plate(license_plate_crop):
    # Use EasyOCR to read the text from the cropped license plate image
    detections = reader.readtext(license_plate_crop)
    for detection in detections:
        bbox, text, score = detection
        text = text.upper().replace(' ', '')
        # Filter out invalid characters
        text = ''.join(filter(str.isalnum, text))
        if is_valid_license_plate(text):
            return text, score
    return None, None

def get_car(license_plate, vehicle_track_ids):
    x1, y1, x2, y2, score, class_id = license_plate
    foundIt = False
    for j in range(len(vehicle_track_ids)):
        xcar1, ycar1, xcar2, ycar2, car_id = vehicle_track_ids[j]
        if x1 > xcar1 and y1 > ycar1 and x2 < xcar2 and y2 < ycar2:
            car_indx = j
            foundIt = True
            break
    if foundIt:
        return vehicle_track_ids[car_indx]
    return -1, -1, -1, -1, -1