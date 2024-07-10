import cv2
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet18
import numpy as np
from PIL import Image

# Load a pre-trained ResNet model
model = resnet18(pretrained=True)
model = model.eval()

# Transformations for the input image
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def get_embedding(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(image)  # Convert numpy array to PIL image
    image = transform(image).unsqueeze(0)

    with torch.no_grad():
        embedding = model(image).squeeze().numpy()

    return embedding

def recognize_face(known_face_image_path, unknown_image_path):
    known_embedding = get_embedding(known_face_image_path)
    unknown_embedding = get_embedding(unknown_image_path)

    # Calculate Euclidean distance between embeddings
    distance = np.linalg.norm(known_embedding - unknown_embedding)

    # Set a threshold for recognizing a face
    threshold = 1.0
    return distance < threshold