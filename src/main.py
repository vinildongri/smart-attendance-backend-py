import cv2
from src.config.settings import settings
from src.services.camera_service import camera_service
from src.services.recognition_service import recognition_service
from src.services.api_service import api_service

def run():
    print("--- 🚀 Starting Smart Attendance AI System ---")
    
    # 1. Load the database of faces
    recognition_service.load_known_faces()
    
    # 2. Start the camera hardware
    if not camera_service.start():
        print("❌ Error: Could not access the camera.")
        return

    print(f"📸 Camera active at: {settings.CAMERA_LOCATION}")
    print("Press 'q' to quit.")

    # Track who we already marked in this session to avoid spamming the API
    processed_roll_numbers = set()

    try:
        while True:
            ret, frame = camera_service.get_frame()
            if not ret:
                break

            # Convert frame to RGB for the AI
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Find faces in the current frame
            import face_recognition
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # Ask the Brain to identify the face
                roll_number, confidence = recognition_service.identify_face(face_encoding)

                # Draw UI Box
                color = (0, 255, 0) if roll_number else (0, 0, 255)
                cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

                if roll_number:
                    label = f"{roll_number} ({confidence}%)"
                    
                    # If this is a new recognition for this session, hit the API
                    if roll_number not in processed_roll_numbers:
                        success = api_service.mark_attendance(roll_number, confidence)
                        if success:
                            processed_roll_numbers.add(roll_number)
                else:
                    label = "Unknown"

                # Draw label text
                cv2.putText(frame, label, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

            # Show the live feed
            cv2.imshow("Smart Attendance - AI Camera", frame)

            # Exit on 'q' key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        print("Cleaning up and closing...")
        camera_service.stop()

if __name__ == "__main__":
    run()