import sys
import cv2
import face_recognition
import json
import tkinter as tk
from tkinter import filedialog
from src.services.recognition_service import recognition_service

def scan_images(file_paths, is_local_test=False):
    if is_local_test:
        print(f"\n--- 🖼️ Local Testing: Scanning {len(file_paths)} Photos ---")
    else:
        pass
    
    recognition_service.load_known_faces()
    marked_present = set()
    recognized_students = []

    for image_path in file_paths:
        if is_local_test: print(f"\n📸 Opening Photo: {image_path}...")
        
        frame = cv2.imread(image_path)
        if frame is None:
            if is_local_test: print(f"   ❌ Error reading {image_path}.")
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if is_local_test: print(f"   👥 Found {len(face_locations)} face(s).")

        for face_encoding in face_encodings:
            roll_number, confidence = recognition_service.identify_face(face_encoding)
            
            if roll_number:
                if roll_number not in marked_present:
                    if is_local_test: print(f"   ✅ Recognized: {roll_number} -> Added to list.")
                    
                    # 🚨 FIXED: No more API calls! Just add to the set and list.
                    marked_present.add(roll_number)
                    recognized_students.append({"rollNumber": roll_number, "name": "Scanned Student"}) 
                else:
                    if is_local_test: print(f"   ⏩ {roll_number} is already marked.")

    # Node.js NEEDS this exact print statement at the very end to read the data.
    print("===RESULT===")
    print(json.dumps({"recognizedStudents": recognized_students}))

if __name__ == "__main__":
    input_files = sys.argv[1:]
    is_local = False

    if len(input_files) == 0:
        is_local = True
        print("🖥️ Local Test Mode Detected: Opening file dialog...")
        
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)

        print("📂 Let's select your photos (Max 5).")
        for i in range(5):
            path = filedialog.askopenfilename(
                title=f"Select Photo {i+1} of 5 (Click 'Cancel' if done)",
                filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
            )
            if not path:
                break
            input_files.append(path)
            
        if len(input_files) == 0:
            print("❌ No files selected. Exiting.")
            sys.exit(1)

    scan_images(input_files, is_local_test=is_local)