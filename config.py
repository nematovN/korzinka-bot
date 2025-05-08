import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Bot token from BotFather
BOT_TOKEN = os.getenv("BOT_TOKEN")

# PostgreSQL Database settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "korzinka")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

# Admin user IDs (list of Telegram user IDs who have admin access)
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]
