import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# CRM Configuration
CRM_API_URL = "https://ya7auto.ru/api.php/crm.deal.add"
CRM_API_TOKEN = os.getenv('CRM_API_TOKEN', 'YOUR_CRM_TOKEN_HERE')
CRM_STAGE_ID = 1
CRM_CONTACT_ID = 4  # Дефолтный контакт, если не удастся создать новый
CRM_USER_CONTACT_ID = 385

# Webhook settings
WEBHOOK_URL = "https://alarmchoice-crm-shibanovmail.amvera.io/"
WEBHOOK_PATH = "/webhook"
PORT = int(os.getenv('PORT', 8080))