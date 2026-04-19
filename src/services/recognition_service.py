import face_recognition
import os
import numpy as np
import traceback

# 1. Protect against missing modules (like python-dotenv)
try:
    from src.config.settings import settings
    THRESHOLD = settings.THRESHOLD
except ImportError:
    print("⚠️ [WARNING] Could not import settings. Using default THRESHOLD of 0.6")
    THRESHOLD = 0.6

class RecognitionService:
    def __init__(self):
        self.known_face_encodings = []
        self.known_roll_numbers = []
        
        # 2. Fix Relative Paths: Dynamically find the absolute path to the root /app folder
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.dataset_path = os.path.join(base_dir, "assets", "dataset")

    def load_known_faces(self):
        """Scans the dataset folder and encodes all images safely."""
        print(f"🧠 [AI] Encoding faces from dataset at: {self.dataset_path}")
        
        if not os.path.exists(self.dataset_path):
            print(f"❌ [ERROR] Dataset folder not found at {self.dataset_path}!")
            return

        try:
            for filename in os.listdir(self.dataset_path):
                if filename.lower().endswith((".jpg", ".png", ".jpeg")):
                    roll_number = os.path.splitext(filename)[0]
                    image_path = os.path.join(self.dataset_path, filename)
                    
                    # 3. Protect against corrupted images crashing the server
                    try:
                        image = face_recognition.load_image_file(image_path)
                        encodings = face_recognition.face_encodings(image)
                        
                        if len(encodings) > 0:
                            self.known_face_encodings.append(encodings[0])
                            self.known_roll_numbers.append(roll_number)
                            print(f"   ✅ Loaded: {roll_number}")
                        else:
                            print(f"   ⚠️ Warning: No face found in {filename}")
                    except Exception as e:
                        print(f"   ❌ ERROR processing {filename}: {e}")
        except Exception as e:
            print(f"❌ [FATAL ERROR] during face loading: {e}")
            traceback.print_exc()

    def identify_face(self, frame_face_encoding):
        """Compares a new face against our database."""
        if not self.known_face_encodings:
            return None, 0.0

        face_distances = face_recognition.face_distance(self.known_face_encodings, frame_face_encoding)
        best_match_index = np.argmin(face_distances)
        distance = face_distances[best_match_index]

        if distance <= THRESHOLD:
            roll_number = self.known_roll_numbers[best_match_index]
            confidence = round((1 - distance) * 100, 2)
            return roll_number, confidence
            
        return None, 0.0

# Create an instance
recognition_service = RecognitionService()