import json
import sys


languages = ["ru", "en"]
try:
    with open("messages.json") as f:
        message_text = json.load(f)
except (FileNotFoundError, KeyError):
    sys.exit(1)
