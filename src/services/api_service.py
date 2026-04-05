import requests
from src.config.settings import settings

class APIService:
    @staticmethod
    def mark_attendance(roll_number, confidence):
        """Sends a POST request to the Node.js backend."""
        payload = {
            "rollNumber": roll_number,
            "aiConfidenceScore": confidence,
            "cameraLocation": settings.CAMERA_LOCATION
        }
        
        try:
            response = requests.post(settings.NODE_API_URL, json=payload)
            if response.status_code in [200, 201]:
                print(f"✅ [API] Success: Marked {roll_number} present.")
                return True
            else:
                print(f"❌ [API] Failed: {response.json().get('message', 'Unknown error')}")
                return False
        except Exception as e:
            print(f"📡 [API] Connection Error: {e}")
            return False

# Create an instance to use elsewhere
api_service = APIService()