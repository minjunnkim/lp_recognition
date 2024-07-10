# EV Charging Station Project

This project is designed to enhance the user experience at EV charging stations by using computer vision and machine learning techniques. It includes face recognition, license plate recognition, and a user-friendly GUI for profile management.

## Project Structure

```
lp_recognition/
├── camera/
│ ├── capture_image.py
│ └── camera_utils.py
├── face_recognition/
│ ├── face_recognition.py
│ └── face_utils.py
├── license_plate_recognition/
│ ├── detect_plate.py
│ ├── ocr_plate.py
│ └── plate_utils.py
├── database/
│ ├── db_setup.py
│ └── db_utils.py
├── gui/
│ ├── login_screen.py
│ └── gui_utils.py
├── images/
│ ├── car_image.jpg
│ ├── known_face.jpg
│ ├── license_plate.jpg
├── main.py
└── requirements.txt
```

## Installation

### Prerequisites

- Python 3.8 or higher
- MongoDB (Local or Atlas)
- Tesseract OCR

### Steps

1. **Clone the repository:**

    ```bash
    git clone https://github.com/minjunnkim/lp_recognition.git
    cd lp_recognition
    ```

2. **Create a virtual environment:**

    ```bash
    python3 -m venv lp_recog_env
    source lp_recog_env/bin/activate  # On Windows: lp_recog_env\Scripts\activate
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Install Tesseract OCR:**

    - **Windows:** [Download and install](https://github.com/UB-Mannheim/tesseract/wiki)
    - **macOS:** 

        ```bash
        brew install tesseract
        ```
    
    - **Linux:**

        ```bash
        sudo apt-get update
        sudo apt-get install tesseract-ocr
        ```

5. **Add Tesseract to PATH (if necessary):**

    - **Windows:**
        Add `C:\Program Files\Tesseract-OCR` to your PATH environment variable.

    - **macOS/Linux:**
        Add the following line to your `.bashrc` or `.bash_profile` file:
        
        ```bash
        export PATH="$PATH:/usr/local/bin/tesseract"
        ```

        Then, reload the profile:

        ```bash
        source ~/.bashrc  # or source ~/.bash_profile
        ```

6. **Set up MongoDB:**
    - Sign up for [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) or install MongoDB locally.
    - Create a new database named `ev_charging`.
    - Create a collection named `profiles`.
    - Update the MongoDB connection URI in your .env file

## Running the Project

1. **Run the database setup script (optional):**

    ```bash
    python database/db_setup.py
    ```

2. **Run the main application:**

    ```bash
    python main.py
    ```

## Project Components

### Face Recognition

Uses PyTorch and torchvision to perform face recognition.

- **face_recognition/face_recognition.py**
- **face_recognition/face_utils.py**

### License Plate Recognition

Detects and recognizes text from license plates using OpenCV and Tesseract OCR.

- **license_plate_recognition/detect_plate.py**
- **license_plate_recognition/ocr_plate.py**
- **license_plate_recognition/plate_utils.py**

### Camera

Captures images using OpenCV.

- **camera/capture_image.py**
- **camera/camera_utils.py**

### Database

Manages user profiles stored in MongoDB.

- **database/db_setup.py**
- **database/db_utils.py**

### GUI

Provides a user-friendly interface for profile management.

- **gui/login_screen.py**
- **gui/gui_utils.py**

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Acknowledgements

- [PyTorch](https://pytorch.org/)
- [torchvision](https://pytorch.org/vision/stable/index.html)
- [OpenCV](https://opencv.org/)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [MongoDB](https://www.mongodb.com/)