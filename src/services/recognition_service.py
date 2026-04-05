import face_recognition
import os
import numpy as np
from src.config.settings import settings

class RecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_roll_numbers = []
        self.dataset_path = "assets/dataset"

    def load_known_faces(self):
        """Scans the dataset folder and encodes all images."""
        print("🧠 [AI] Encoding faces from dataset...")
        
        for filename in os.listdir(self.dataset_path):
            if filename.endswith((".jpg", ".png", ".jpeg")):
                # The filename (without .jpg) is used as the Roll Number
                roll_number = os.path.splitext(filename)[0]
                
                image_path = os.path.join(self.dataset_path, filename)
                image = face_recognition.load_image_file(image_path)
                
                # Get the 128-d face encoding
                encodings = face_recognition.face_encodings(image)
                
                if len(encodings) > 0:
                    self.known_face_encodings.append(encodings[0])
                    self.known_roll_numbers.append(roll_number)
                    print(f"   - Loaded: {roll_number}")
                else:
                    print(f"   - ⚠️ Warning: No face found in {filename}")

    def identify_face(self, frame_face_encoding):
        """Compares a new face against our database."""
        if not self.known_face_encodings:
            return None, 0.0

        # Calculate distances (Lower is a better match)
        face_distances = face_recognition.face_distance(self.known_face_encodings, frame_face_encoding)
        best_match_index = np.argmin(face_distances)
        
        distance = face_distances[best_match_index]

        # Check if the best match is within our threshold (0.6)
        if distance <= settings.THRESHOLD:
            roll_number = self.known_roll_numbers[best_match_index]
            confidence = round((1 - distance) * 100, 2)
            return roll_number, confidence
            
        return None, 0.0

# Create an instance
recognition_service = RecognitionService()