import cv2

def capture_image(filename='images/car_image.jpg'):
    # Initialize the camera
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise Exception("Could not open video device")

    # Capture a frame
    ret, frame = camera.read()
    camera.release()

    # Save the image
    cv2.imwrite(filename, frame)
    return filename