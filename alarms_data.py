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
    Поиск подходящих сигнализаций по критериям

    Args:
        autostart (bool): Нужен ли автозапуск
        gsm (bool): Управление через приложение (True) или брелок (False)
        gps (bool): Нужен ли GPS

    Returns:
        list: Список подходящих сигнализаций
    """
    matching = []

    for alarm in ALARMS:
        if (alarm['autostart'] == autostart and
                alarm['gsm'] == gsm and
                alarm['gps'] == gps):
            matching.append(alarm)

    return matching


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

    # Пример 1: Без автозапуска, брелок, без GPS
    result = find_matching_alarms(False, False, False)
    print(f"\nБез автозапуска, брелок, без GPS: {len(result)} шт.")
    for alarm in result:
        print(f"  - {alarm['name']} ({alarm['price']})")

    # Пример 2: С автозапуском, приложение, с GPS
    result = find_matching_alarms(True, True, True)
    print(f"\nС автозапуском, приложение, с GPS: {len(result)} шт.")
    for alarm in result:
        print(f"  - {alarm['name']} ({alarm['price']})")

    # Все сигнализации Pandora
    pandora_alarms = get_alarms_by_brand('Pandora')
    print(f"\nВсего Pandora: {len(pandora_alarms)} шт.")

    # Сигнализации в диапазоне цен 15-20 тыс.
    price_range_alarms = get_alarms_by_price_range(15000, 20000)
    print(f"\nВ диапазоне 15-20 тыс.: {len(price_range_alarms)} шт.")
    for alarm in price_range_alarms:
        print(f"  - {alarm['name']} ({alarm['price']})")