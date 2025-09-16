# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Webhook Configuration
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-app-name.amvera.io')
WEBHOOK_PORT = int(os.getenv('PORT', '8443'))
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"  # Добавляем WEBHOOK_PATH

# CRM Configuration
CRM_API_URL = "https://ya7auto.ru/api.php/crm.deal.add"
CRM_API_TOKEN = os.getenv('CRM_API_TOKEN', 'YOUR_CRM_TOKEN_HERE')
CRM_STAGE_ID = 1
CRM_CONTACT_ID = 4
CRM_USER_CONTACT_ID = 385