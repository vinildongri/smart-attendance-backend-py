import os
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

class Settings:
    NODE_API_URL = os.getenv("NODE_API_URL")
    CAMERA_ID = int(os.getenv("CAMERA_ID", 0))
    CAMERA_LOCATION = os.getenv("CAMERA_LOCATION", "Unknown_Gate")
    # Face distance: Lower is stricter (0.5 is very strict, 0.7 is loose)
    THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.6))

# Create a single instance to use across the app
settings = Settings()