import os

BOT_TOKEN = os.environ.get("BOT_TOKEN", "5618782891:AAEI6n09tMBpmUrND3twHpxQxHlAVczTF5Y")
API_ID = int(os.environ.get("API_ID", "10098309"))
API_HASH = os.environ.get("API_HASH", "aaacac243dddc9f0433c89cab8efe323")
LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1001587861988"))
AUTH_USERS = set(int(x) for x in os.environ.get("AUTH_USERS", "2056407064").split())
DB_URL = os.environ.get("DB_URL", "mongodb+srv://codexun:TeamCodexun07@codexun.egmx5.mongodb.net/?retryWrites=true&w=majority")
DB_NAME = os.environ.get("DB_NAME", "ThumbnailBot")
BROADCAST_AS_COPY = bool(os.environ.get("BROADCAST_AS_COPY", True))
