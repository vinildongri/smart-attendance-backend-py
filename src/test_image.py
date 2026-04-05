import cv2
import face_recognition
import tkinter as tk
from tkinter import filedialog, messagebox
from src.services.recognition_service import recognition_service
from src.services.api_service import api_service

def scan_selected_images():
    # 1. Setup the UI Window
    root = tk.Tk()
    root.withdraw()  
    root.attributes('-topmost', True) 

    file_paths = []
    print("📂 Let's select your photos one by one (Max 5).")

    # Loop to ask for photos individually
    for i in range(5):
        path = filedialog.askopenfilename(
            title=f"Select Photo {i+1} of 5 (Click 'Cancel' if you are done)",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        
        # If they hit cancel or close the window
        if not path:
            break
            
        file_paths.append(path)
        print(f"   📎 Added: {path.split('/')[-1]}")

    num_files = len(file_paths)
    
    # Check the rules!
    if num_files < 3:
        print(f"❌ You only selected {num_files} photo(s). You need at least 3. Exiting...")
        return

    print(f"\n--- 🖼️ Scanning {num_files} Selected Photos ---")
    
    # 2. Load the database of known faces
    recognition_service.load_known_faces()
    marked_present = set()

    # 3. Loop through the exact files you clicked on
    for image_path in file_paths:
        filename = image_path.split("/")[-1] 
        print(f"\n📸 Opening Photo: {filename}...")
        
        frame = cv2.imread(image_path)
        if frame is None:
            print(f"   ❌ Error reading {filename}.")
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        print(f"   👥 Found {len(face_locations)} face(s) in this photo.")

        for face_encoding in face_encodings:
            roll_number, confidence = recognition_service.identify_face(face_encoding)
            
            if roll_number:
                if roll_number not in marked_present:
                    print(f"   ✅ Recognized: {roll_number} ({confidence}%) -> Sending to API...")
                    success = api_service.mark_attendance(roll_number, confidence)
                    if success:
                        marked_present.add(roll_number)
                else:
                    print(f"   ⏩ {roll_number} ({confidence}%) is already marked present today. Skipping API.")
            else:
                print("   ❌ Unknown Face detected.")

    print("\n🎉 --- Batch Processing Complete ---")
    print(f"Total unique students marked present: {len(marked_present)}")

if __name__ == "__main__":
    scan_selected_images()