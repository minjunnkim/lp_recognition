import tkinter as tk
from tkinter import simpledialog, messagebox
from database.db_utils import get_database, insert_profile, get_profiles
from camera.capture_image import capture_image
from license_plate_recognition.detect_plate import detect_plate
from license_plate_recognition.ocr_plate import ocr_license_plate
from face_recognition.face_recognition import recognize_face

def create_profile(db, license_plate):
    new_profile = simpledialog.askstring("New Profile", "Enter profile name:")
    if new_profile:
        profile_data = {
            "license_plate": license_plate,
            "profiles": [{"name": new_profile}]
        }
        insert_profile(db, profile_data)
        # Update the listbox
        profile_listbox.insert(tk.END, new_profile)

def capture_and_process_image():
    # Capture the image
    image_path = capture_image(filename='images/car_image.jpg')

    # Detect license plate
    plate_image_path = detect_plate(image_path)

    # Perform OCR on the license plate
    license_plate_text = ocr_license_plate(plate_image_path)
    print("Detected License Plate Number:", license_plate_text)
    
    # Return the detected license plate text
    return license_plate_text

def capture_and_recognize_face():
    # Capture the image
    image_path = capture_image(filename='images/unknown_face.jpg')

    # Perform face recognition
    known_face_image = 'images/known_face.jpg'  # Path to known face image
    if recognize_face(known_face_image, image_path):
        print("Face recognized")
        return True
    else:
        print("Face not recognized")
        return False

def main():
    db = get_database()
    root = tk.Tk()
    root.title("EV Charging Station Login")

    def capture_image_and_load_profiles():
        # Capture image and process it
        license_plate_text = capture_and_process_image()
        
        # Load profiles associated with the license plate
        profiles_data = get_profiles(db, license_plate_text)

        # Clear existing profiles in the listbox
        profile_listbox.delete(0, tk.END)

        if profiles_data:
            for profile in profiles_data['profiles']:
                profile_listbox.insert(tk.END, profile['name'])
        else:
            messagebox.showinfo("Info", "No profiles found for the detected license plate.")

    def authenticate_user_and_load_profiles():
        if capture_and_recognize_face():
            capture_image_and_load_profiles()
        else:
            messagebox.showerror("Error", "Face not recognized.")

    global profile_listbox
    profile_listbox = tk.Listbox(root)
    profile_listbox.pack()

    capture_image_button = tk.Button(root, text="Capture Image & Load Profiles", command=authenticate_user_and_load_profiles)
    capture_image_button.pack()

    def create_new_profile():
        selected_license_plate = capture_and_process_image()
        create_profile(db, selected_license_plate)

    create_profile_button = tk.Button(root, text="Create Profile", command=create_new_profile)
    create_profile_button.pack()

    def select_profile():
        selected_profile = profile_listbox.get(tk.ACTIVE)
        print("Selected profile:", selected_profile)

    select_profile_button = tk.Button(root, text="Select Profile", command=select_profile)
    select_profile_button.pack()

    root.mainloop()

if __name__ == "__main__":
    main()