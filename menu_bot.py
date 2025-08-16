import os
import sys
import requests
import pytesseract
from PIL import Image

# Load Teams webhook from environment
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

if not TEAMS_WEBHOOK:
    print("❌ ERROR: TEAMS_WEBHOOK is not set in GitHub Secrets")
    sys.exit(1)

# OCR from image
image_path = "menuuu.jpeg"
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
payload = {
    "text": menu_message
}

resp = requests.post(TEAMS_WEBHOOK, json=payload)

if resp.status_code != 200:
    print(f"❌ Failed to send message: {resp.status_code}, {resp.text}")
else:
    print("✅ Menu posted successfully!")
