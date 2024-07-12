import tkinter as tk
from tkinter import messagebox
from database.db_utils import get_database, get_profiles
from camera.capture_image import capture_image
from license_plate_recognition.detect_plate_yolov8 import detect_and_track_vehicles
from gui.profiles_screen import show_profiles_screen

def capture_and_process_image():
    # Capture the image
    image_path = capture_image(filename='images/car_image.jpg')

    # Detect license plate
    license_plate_text = detect_and_track_vehicles(image_path)

    if license_plate_text:
        print("Detected License Plate Number:", license_plate_text)
        return license_plate_text
    else:
        messagebox.showerror("Error", "License plate not detected.")
        return None

def main():
    db = get_database()
    root = tk.Tk()
    root.title("EV Charging Station Login")

    def capture_image_and_load_profiles():
        license_plate_text = capture_and_process_image()
        
        if license_plate_text:
            confirm_license_plate(license_plate_text)

    def confirm_license_plate(license_plate_text):
        confirm_window = tk.Toplevel(root)
        confirm_window.title("Confirm License Plate")

        tk.Label(confirm_window, text=f"Detected License Plate: {license_plate_text}").pack(pady=10)
        
        def on_confirm():
            confirm_window.destroy()
            # Load profiles associated with the license plate
            profiles_data = get_profiles(db, license_plate_text)

            if profiles_data:
                profiles = profiles_data['profiles']
            else:
                profiles = []

            show_profiles_screen(root, db, license_plate_text, profiles)
        
        def on_retry():
            confirm_window.destroy()
            capture_image_and_load_profiles()

        tk.Button(confirm_window, text="Confirm", command=on_confirm).pack(pady=5)
        tk.Button(confirm_window, text="Retry", command=on_retry).pack(pady=5)

    capture_image_button = tk.Button(root, text="Capture Image & Load Profiles", command=capture_image_and_load_profiles)
    capture_image_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()