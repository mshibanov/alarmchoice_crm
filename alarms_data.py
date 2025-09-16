# alarms_data.py
ALARMS = [
    {
        "name": "Pandora DX-40R",
        "brand": "Pandora",
        "price": "12 961 ₽",
        "autostart": False,
        "remote": True,
        "gsm": False,
        "gps": False,
        "tag": "Нет",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandora-dx-40r/"
    },
    {
        "name": "Pandora DX-40RS",
        "brand": "Pandora",
        "price": "13 490 ₽",
        "autostart": True,
        "remote": True,
        "gsm": False,
        "gps": False,
        "tag": "Нет",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandora-dx-40rs/"
    },
    {
        "name": "PanDECT X-1800L v4 Light",
        "brand": "Pandora",
        "price": "16 100 ₽",
        "autostart": True,
        "remote": False,
        "gsm": True,
        "gps": False,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandect-x-1800l-v4-light/"
    },
    {
        "name": "Pandora VX 4G Light",
        "brand": "Pandora",
        "price": "19 320 ₽",
        "autostart": True,
        "remote": False,
        "gsm": True,
        "gps": False,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandora-vx-4g-light/"
    },
    {
        "name": "Pandora VX-4G GPS v2",
        "brand": "Pandora",
        "price": "29 360 ₽",
        "autostart": True,
        "remote": False,
        "gsm": True,
        "gps": True,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandora-vx-4g-gps-v2/"
    },
    {
        "name": "Pandora VX 3100",
        "brand": "Pandora",
        "price": "31 343 ₽",
        "autostart": True,
        "remote": True,
        "gsm": True,
        "gps": True,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/pandora-vx-3100/"
    },
    {
        "name": "StarLine A63 v2 ECO",
        "brand": "StarLine",
        "price": "9 150 ₽",
        "autostart": False,
        "remote": True,
        "gsm": False,
        "gps": False,
        "tag": "Нет",
        "link": "https://ya7auto.ru/auto-security/car-alarms/starline-a63-v2-eco/"
    },
    {
        "name": "StarLine А93 v2 ECO",
        "brand": "StarLine",
        "price": "11 800 ₽",
        "autostart": True,
        "remote": True,
        "gsm": False,
        "gps": False,
        "tag": "Нет",
        "link": "https://ya7auto.ru/auto-security/car-alarms/starline-a93-v2-eco/"
    },
    {
        "name": "StarLine S96 v2 ECO",
        "brand": "StarLine",
        "price": "19 450 ₽",
        "autostart": True,
        "remote": False,
        "gsm": True,
        "gps": False,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/starline-s96-v2-eco/"
    },
    {
        "name": "StarLine S96 V2 LTE GPS",
        "brand": "StarLine",
        "price": "28 100 ₽",
        "autostart": True,
        "remote": False,
        "gsm": True,
        "gps": True,
        "tag": "Да",
        "link": "https://ya7auto.ru/auto-security/car-alarms/starline-s96-v2-lte-gps/"
    }
]


def find_matching_alarms(autostart, gsm, gps):
    """
    Поиск подходящих сигнализаций по критериям с системой баллов

    Args:
        autostart (bool): Нужен ли автозапуск
        gsm (bool): Управление через приложение (True) или брелок (False)
        gps (bool): Нужен ли GPS

    Returns:
        list: Отсортированный список подходящих сигнализаций с баллами соответствия
    """
    scored_alarms = []

    for alarm in ALARMS:
        score = 0

        # Основные критерии (больший вес)
        if alarm['autostart'] == autostart:
            score += 3
        if alarm['gsm'] == gsm:
            score += 3
        if alarm['gps'] == gps:
            score += 3

        # Дополнительные критерии (меньший вес)
        if alarm['autostart'] and autostart:  # Если нужен автозапуск и он есть
            score += 1
        if alarm['gsm'] and gsm:  # Если нужно приложение и оно есть
            score += 1
        if alarm['gps'] and gps:  # Если нужен GPS и он есть
            score += 1

        # Штраф за отсутствие нужных функций
        if not alarm['autostart'] and autostart:
            score -= 2
        if not alarm['gsm'] and gsm:
            score -= 2
        if not alarm['gps'] and gps:
            score -= 2

        # Добавляем систему в список с баллом
        scored_alarms.append({
            'alarm': alarm,
            'score': score,
            'perfect_match': (alarm['autostart'] == autostart and
                              alarm['gsm'] == gsm and
                              alarm['gps'] == gps)
        })

    # Фильтруем системы с положительным баллом или идеальные совпадения
    filtered_alarms = [item for item in scored_alarms if item['score'] > 0 or item['perfect_match']]

    # Сортируем по баллам (по убыванию)
    filtered_alarms.sort(key=lambda x: x['score'], reverse=True)

    # Берем топ-3 рекомендации
    top_alarms = [item['alarm'] for item in filtered_alarms[:3]]

    return top_alarms


def get_all_alarms():
    """Получить все сигнализации"""
    return ALARMS


def get_alarms_by_brand(brand):
    """Получить сигнализации по бренду"""
    return [alarm for alarm in ALARMS if alarm['brand'].lower() == brand.lower()]


def get_alarms_by_price_range(min_price, max_price):
    """Получить сигнализации в диапазоне цен"""

    def parse_price(price_str):
        # Убираем пробелы и символ валюты, преобразуем в число
        return float(price_str.replace(' ', '').replace('₽', '').strip())

    return [alarm for alarm in ALARMS
            if min_price <= parse_price(alarm['price']) <= max_price]


# Пример использования функций
if __name__ == "__main__":
    # Тестирование поиска
    print("=== Тест поиска сигнализаций ===")

    # Пример: С автозапуском, брелок, с GPS (идеальное совпадение - Pandora VX 3100)
    result = find_matching_alarms(True, False, True)
    print(f"\nС автозапуском, брелок, с GPS: {len(result)} шт.")
    for alarm in result:
        print(f"  - {alarm['name']} (автозапуск: {alarm['autostart']}, GSM: {alarm['gsm']}, GPS: {alarm['gps']})")

    # Пример 2: Без автозапуска, брелок, без GPS
    result = find_matching_alarms(False, False, False)
    print(f"\nБез автозапуска, брелок, без GPS: {len(result)} шт.")
    for alarm in result:
        print(f"  - {alarm['name']} ({alarm['price']})")