import os
import sys
import requests
import pytesseract
from PIL import Image
import glob

# Load Teams webhook from environment
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

if not TEAMS_WEBHOOK:
    print("❌ ERROR: TEAMS_WEBHOOK is not set in GitHub Secrets")
    sys.exit(1)

# Find the latest uploaded photo in menuphotos/
files = glob.glob("menuphotos/*")
if not files:
    print("❌ No image found in menuphotos/")
    sys.exit(1)

# Pick the most recent file
image_path = max(files, key=os.path.getctime)
print(f"📸 Processing file: {image_path}")

# OCR from image
text = pytesseract.image_to_string(Image.open(image_path))

# Clean text lines
menu_items = []
for line in text.splitlines():
    line = line.strip()
    if line and not line.lower().startswith("menu is subject"):
        menu_items.append(line)

# Format Teams message
menu_message = "**📋 Today's Menu**\n\n" + "\n".join(f"- {item}" for item in menu_items)

# Send to Teams
payload = {"text": menu_message}
resp = requests.post(TEAMS_WEBHOOK, json=payload)

if resp.status_code != 200:
    print(f"❌ Failed to send message: {resp.status_code}, {resp.text}")
else:
    print("✅ Menu posted successfully!")
