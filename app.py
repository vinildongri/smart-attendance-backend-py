from flask import Flask, request, jsonify
import cv2
import numpy as np
import face_recognition
import os
from src.services.recognition_service import recognition_service

app = Flask(__name__)

# Load known faces once when the server starts up, not on every request!
print("Loading known faces...")
recognition_service.load_known_faces()
print("Faces loaded successfully.")

@app.route('/api/recognize', methods=['POST'])
def recognize():
    if 'images' not in request.files:
        return jsonify({"success": False, "message": "No images uploaded."}), 400
    
    files = request.files.getlist('images')
    marked_present = set()
    recognized_students = []

    for file in files:
        # 1. Read the image directly from memory (faster, no temp files needed)
        file_bytes = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        
        if frame is None:
            continue

        # 2. Process with face_recognition
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        # 3. Identify faces
        for face_encoding in face_encodings:
            roll_number, confidence = recognition_service.identify_face(face_encoding)
            
            if roll_number and roll_number not in marked_present:
                marked_present.add(roll_number)
                recognized_students.append({
                    "rollNumber": roll_number, 
                    "name": "Scanned Student"
                })

    return jsonify({
        "success": True,
        "recognizedStudents": recognized_students
    })

# Render needs to be able to bind to the dynamic PORT environment variable
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)