import requests
import json
from datetime import datetime, timedelta
from config import CRM_API_URL, CRM_API_TOKEN, CRM_STAGE_ID, CRM_CONTACT_ID, CRM_USER_CONTACT_ID


def create_crm_contact(user_data):
    """Создание контакта в CRM"""

    contact_data = {
        "firstname": user_data.get('username', 'Неизвестно'),
        "lastname": "",
        "phone": user_data.get('phone', ''),
        "email": "",
        "sex": "m",
        "company": "",
        "jobtitle": ""
    }

    headers = {
        "Authorization": f"Bearer {CRM_API_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    # Подготовка данных в формате, требуемом API
    api_data = []
    for field_id, value in contact_data.items():
        if value:  # Отправляем только заполненные поля
            api_data.append({
                "field": field_id,
                "value": value
            })

    try:
        response = requests.post(
            "https://ya7auto.ru/api.php/crm.contact.add",
            headers=headers,
            data=json.dumps(api_data),
            timeout=30
        )

        if response.status_code == 200:
            result = response.json()
            if isinstance(result, dict) and 'error' in result:
                print(f"Ошибка создания контакта: {result.get('error_description', 'Неизвестная ошибка')}")
                return None
            else:
                print(f"Контакт успешно создан! ID: {result}")
                return result
        else:
            print(f"HTTP ошибка при создании контакта: {response.status_code} - {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Ошибка соединения при создании контакта: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON при создании контакта: {e}")
        return None


def create_crm_deal(user_data, recommended_alarms):
    """Создание сделки в CRM"""

    # Сначала создаем контакт
    contact_id = create_crm_contact(user_data)
    if not contact_id:
        # Если не удалось создать контакт, используем дефолтный
        contact_id = CRM_CONTACT_ID
        print(f"Используем дефолтный contact_id: {contact_id}")

    description = f"""
Имя: {user_data['username']}
Телефон: {user_data.get('phone', 'Не указан')}

Выбор клиента:
• Автозапуск: {'Да' if user_data['autostart'] else 'Нет'}
• Управление: {'Приложение' if user_data['gsm'] else 'Брелок'}
• GPS: {'Да' if user_data['gps'] else 'Нет'}

Рекомендованные сигнализации:
{', '.join([alarm['name'] for alarm in recommended_alarms])}
"""

    deal_data = {
        "name": f"AlarmChoice - {user_data['username']}",
        "stage_id": CRM_STAGE_ID,
        "contact_id": contact_id,
        "user_contact_id": CRM_USER_CONTACT_ID,
        "description": description,
        "expected_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "amount": 0,
        "currency_id": "RUB",
        "contact_label": "Заказчик"
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CRM_API_TOKEN}"
    }

    try:
        response = requests.post(CRM_API_URL, headers=headers, json=deal_data, timeout=30)
        return response.status_code in [200, 201]
    except Exception as e:
        print(f"Ошибка при создании сделки: {e}")
        return False