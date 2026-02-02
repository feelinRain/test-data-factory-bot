# generators.py
from faker import Faker
import random
import string

# Инициализируем Faker только для RU и EN
fake_ru = Faker('ru_RU')
fake_en = Faker('en_US')

def generate_name_address(locale='ru'):
    """Генерация ФИО и адреса для указанной локали."""
    fakers = {'ru': fake_ru, 'en': fake_en}
    
    # Нормализуем локаль: приводим к нижнему регистру, если это строка
    if isinstance(locale, str):
        locale = locale.lower()
    
    # Если локаль не 'ru' или 'en', используем 'ru' по умолчанию
    if locale not in fakers:
        locale = 'ru'
    
    faker = fakers[locale]

    # Генерируем данные
    full_name = faker.name()
    address = faker.address().replace("\n", ", ")
    
    # Генерируем телефон в зависимости от локали
    if locale == 'ru':
        # Для России: +7 (XXX) XXX-XX-XX
        area_code = faker.random_int(900, 999)  # 900-999 - мобильные коды
        first_part = faker.random_int(100, 999)
        second_part = faker.random_int(10, 99)
        third_part = faker.random_int(10, 99)
        phone = f"+7 ({area_code}) {first_part}-{second_part}-{third_part}"
        
        # С вероятностью 20% добавляем добавочный номер (для офисных телефонов)
        if faker.random_int(1, 100) <= 20:
            extension = faker.random_int(1000, 9999)
            phone += f" доб. {extension}"
            
    elif locale == 'en':
        # Для США: (XXX) XXX-XXXX
        area_code = faker.random_int(200, 999)  # 200-999 - допустимые коды зон в US
        exchange_code = faker.random_int(200, 999)  # 200-999 - центральный офис коды
        subscriber_number = faker.random_int(1000, 9999)  # 1000-9999 - номер абонента
        phone = f"({area_code}) {exchange_code}-{subscriber_number}"
        
        # С вероятностью 10% добавляем код страны
        if faker.random_int(1, 100) <= 10:
            phone = f"+1 {phone}"
    else:
        phone = faker.phone_number()

    data = {
        'full_name': full_name,
        'address': address,
        'phone': phone,
        'locale': locale.upper()
    }
    return data

# Остальные функции остаются без изменений
def generate_credit_card():
    """Генерация номера кредитной карты с помощью алгоритма Луна."""
    # Генерируем 15 случайных цифр (без последней контрольной)
    card_number = [str(random.randint(0, 9)) for _ in range(15)]

    # Алгоритм Луна для вычисления контрольной цифры (16-й)
    total = 0
    for i, digit in enumerate(card_number):
        n = int(digit)
        if (i + 1) % 2 != 0:  # Нечетные позиции (для алгоритма, считая с 1)
            n *= 2
            if n > 9:
                n -= 9
        total += n

    check_digit = (10 - (total % 10)) % 10
    card_number.append(str(check_digit))

    # Форматируем как настоящую карту (XXXX XXXX XXXX XXXX)
    formatted_number = ''.join(card_number)
    formatted_number = ' '.join([formatted_number[i:i+4] for i in range(0, 16, 4)])

    # Дополнительные данные карты
    card_type = random.choice(['Visa', 'MasterCard', 'Mir'])
    expiry_date = f"{random.randint(1, 12):02d}/{random.randint(23, 30)}"
    cvv = f"{random.randint(0, 999):03d}"

    return {
        'number': formatted_number,
        'type': card_type,
        'expiry': expiry_date,
        'cvv': cvv
    }

def generate_boundary_strings():
    """Генерация строк с граничными значениями и инъекциями."""
    # Создаем список словарей для удобства
    strings = [
        {
            'title': '📏 Строка ровно 255 символов',
            'value': 'A' * 255,
            'description': 'Проверка ограничения длины (255 символов)'
        },
        {
            'title': '⚠️ Спецсимволы',
            'value': '!@#$%^&*()_+{}|:"<>?[]\\;\',./`~',
            'description': 'Строка со специальными символами'
        },
        {
            'title': '🥷 SQL-инъекция',
            'value': "' OR '1'='1'; --",
            'description': 'Базовый пример SQL-инъекции (для тестирования)'
        },
        {
            'title': '🛡️ XSS-инъекция',
            'value': '<script>alert("XSS")</script>',
            'description': 'Базовый пример XSS-инъекции (для тестирования)'
        },
        {
            'title': '⚫ Пустая строка',
            'value': '',
            'description': 'Пустая строка для проверки обязательных полей'
        },
        {
            'title': '🐌 Очень длинная строка (1000 символов)',
            'value': 'B' * 1000,
            'description': 'Строка из 1000 символов (тест на производительность)'
        },
        {
            'title': '🌍 Эмодзи и юникод',
            'value': 'Тест € ¥ 🌎 𐌀 𐌁 𐌂 Привет 你好',
            'description': 'Строка с эмодзи и мультиязычными символами'
        },
        {
            'title': '🔤 Смешанный регистр',
            'value': 'Тест Test тест TEST 123',
            'description': 'Строка с символами в разном регистре'
        },
        {
            'title': '📝 Переносы строк и табуляция',
            'value': 'Первая строка\nВторая строка\tТабуляция\rВозврат каретки',
            'description': 'Строка с управляющими символами'
        }
    ]
    return strings

def generate_temp_email():
    """Генерация временного email-адреса (на основе случайной строки)."""
    domains = ["temp-mail.org", "10minutemail.com", "guerrillamail.com", "yopmail.com"]
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=10))
    domain = random.choice(domains)
    email = f"{username}@{domain}"

    return {
        'email': email,
        'note': "Это домен для временной почты. Проверьте сайт сервиса для доступа к письмам."
    }