import os, glob, pytesseract
from PIL import Image
import requests

TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

# Find latest photo
files = glob.glob("menuphotos/*")
latest = max(files, key=os.path.getctime)

# OCR
text = pytesseract.image_to_string(Image.open(latest))

# Build Teams message
message = {
    "text": f"📋 Today's Menu\n\n{text}"
}

# Post to Teams
resp = requests.post(TEAMS_WEBHOOK, json=message)
print("Posted:", resp.status_code, resp.text)
