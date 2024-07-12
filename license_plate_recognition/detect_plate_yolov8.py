import cv2
import numpy as np
from ultralytics import YOLO
from .sort import Sort
from .utils import get_car, read_license_plate

def load_models():
    coco_model = YOLO('yolov8n.pt')  # YOLO model for vehicle detection
    license_plate_detector = YOLO('license_plate_detector.pt')  # Path to the provided model
    return coco_model, license_plate_detector

def preprocess_image(license_plate_crop):
    # Convert to grayscale
    license_plate_crop_gray = cv2.cvtColor(license_plate_crop, cv2.COLOR_BGR2GRAY)
    # Resize image
    license_plate_crop_resized = cv2.resize(license_plate_crop_gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
    # Adaptive thresholding
    license_plate_crop_thresh = cv2.adaptiveThreshold(
        license_plate_crop_resized, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    # Increase contrast
    alpha = 2.0  # Simple contrast control
    beta = 0     # Simple brightness control
    license_plate_crop_contrast = cv2.convertScaleAbs(license_plate_crop_thresh, alpha=alpha, beta=beta)
    return license_plate_crop_contrast

def filter_contours(image, contours):
    height, width = image.shape
    filtered_contours = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = w / float(h)
        area = w * h
        # Filter by aspect ratio and area
        if 0.2 < aspect_ratio < 1.0 and 100 < area < 5000:
            # Ignore regions too close to the edges
            if x > 0.05 * width and (x + w) < 0.95 * width and y > 0.05 * height and (y + h) < 0.95 * height:
                filtered_contours.append(contour)
    return filtered_contours

def detect_and_track_vehicles(image_path):
    coco_model, license_plate_detector = load_models()
    image = cv2.imread(image_path)
    
    mot_tracker = Sort()

    # Detect vehicles
    detections = coco_model(image)[0]
    detections_ = []
    for detection in detections.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = detection
        if int(class_id) in [2, 3, 5, 7]:  # Class IDs for vehicles
            detections_.append([x1, y1, x2, y2])

    # Track vehicles
    track_ids = mot_tracker.update(np.asarray(detections_))

    # Detect license plates
    license_plates = license_plate_detector(image)[0]
    for license_plate in license_plates.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = license_plate
        xcar1, ycar1, xcar2, ycar2, car_id = get_car(license_plate, track_ids)

        if car_id != -1:
            license_plate_crop = image[int(y1):int(y2), int(x1):int(x2), :]
            cv2.imwrite('images/license_plate.jpg', license_plate_crop)

            # Preprocess license plate image for better OCR accuracy
            preprocessed_image = preprocess_image(license_plate_crop)

            # Find contours and filter by size and aspect ratio
            contours, _ = cv2.findContours(preprocessed_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            filtered_contours = filter_contours(preprocessed_image, contours)

            # Create a mask with filtered contours
            mask = np.zeros_like(preprocessed_image)
            if filtered_contours:  # Ensure there are filtered contours
                cv2.drawContours(mask, filtered_contours, -1, (255), thickness=cv2.FILLED)
            cv2.imwrite('images/license_plate_mask.jpg', mask)

            # Apply mask to the preprocessed image
            masked_license_plate = cv2.bitwise_and(preprocessed_image, preprocessed_image, mask=mask)
            cv2.imwrite('images/license_plate_masked.jpg', masked_license_plate)

            # Read license plate number
            license_plate_text, license_plate_text_score = read_license_plate(masked_license_plate)
            
            # Print for debugging
            print(f"Detected text: {license_plate_text}, Score: {license_plate_text_score}")
            
            if license_plate_text:
                return license_plate_text
    return None

# Path to the uploaded image
image_path = 'images/car_image.jpg'

# Detecting the license plate using YOLOv8
detected_plate_text = detect_and_track_vehicles(image_path)
print(f"Detected License Plate Text: {detected_plate_text}")