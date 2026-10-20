# Food Menu → Teams

Posts the cafeteria menu to Microsoft Teams. Upload a photo of the menu, and a GitHub Action reads it with OCR and posts the items to a Teams channel.

## How it works
1. Push a photo to `menuphotos/` on `main`.
2. The workflow `.github/workflows/menu_updates.yml` installs Tesseract and runs `menu_bot.py`.
3. The script takes the newest image, extracts text with `pytesseract`, drops the "menu is subject to change" line, and posts a bulleted **Today's Menu** to Teams.

`ocr_menu.py` is a simpler variant that reads from `menu_photos/` and adds the date to the message.

## Setup
1. Create an incoming webhook in your Teams channel.
2. Add it as the repo secret **`TEAMS_WEBHOOK`** (Settings → Secrets and variables → Actions).

## Run locally
```bash
sudo apt-get install tesseract-ocr
pip install -r requirements.txt
export TEAMS_WEBHOOK="<your webhook URL>"
python menu_bot.py
```

## Tech stack
Python 3.10, pytesseract, Pillow, requests and GitHub Actions.
