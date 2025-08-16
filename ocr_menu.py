import os
import pytesseract
from PIL import Image
import requests
from datetime import datetime

# Get Teams webhook from secret
TEAMS_WEBHOOK = os.getenv("TEAMS_WEBHOOK")

def get_latest_photo(folder="menu_photos"):
    files = [os.path.join(folder, f) for f in os.listdir(folder) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    if not files:
        return None
    return max(files, key=os.path.getctime)  # latest file

def extract_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img)
    return text.strip()

def format_message(text):
    today = datetime.now().strftime("%A, %d %B %Y")
    return f"🍴 Today's Cafeteria Menu – {today}\n\n{text}"

def post_to_teams(message):
    if not TEAMS_WEBHOOK:
        print("❌ Teams webhook not found.")
        return
    payload = {"text": message}
    try:
        response = requests.post(TEAMS_WEBHOOK, json=payload)
        print("✅ Posted to Teams:", response.status_code)
    except Exception as e:
        print("❌ Error posting:", e)

if __name__ == "__main__":
    photo = get_latest_photo()
    if photo:
        print(f"📷 Using photo: {photo}")
        text = extract_text(photo)
        message = format_message(text)
        post_to_teams(message)
    else:
        print("❌ No photo found in menu_photos/")
