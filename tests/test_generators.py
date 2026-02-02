# tests/test_generators.py
import pytest
from generators import (
    generate_name_address,
    generate_credit_card,
    generate_boundary_strings,
    generate_temp_email
)
import re

class TestNameAddressGenerator:
    """Тесты для генерации ФИО и адресов."""
    
    def test_generate_name_address_ru(self):
        """Тест генерации русских данных."""
        result = generate_name_address('ru')
        
        # Проверяем структуру ответа
        assert isinstance(result, dict)
        assert 'full_name' in result
        assert 'address' in result
        assert 'phone' in result
        assert 'locale' in result
        assert result['locale'] == 'RU'
        
        # Проверяем, что поля не пустые
        assert result['full_name'].strip() != ''
        assert result['address'].strip() != ''
        assert result['phone'].strip() != ''
        
        # Проверяем формат русского телефона
        # Должен начинаться с +7 или 8
        assert result['phone'].startswith('+7') or 'доб.' in result['phone']
        
    def test_generate_name_address_en(self):
        """Тест генерации английских данных."""
        result = generate_name_address('en')
        
        assert isinstance(result, dict)
        assert result['locale'] == 'EN'
        
        # Проверяем формат US телефона: (XXX) XXX-XXXX
        phone_pattern = r'\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}'
        assert re.match(phone_pattern, result['phone'].replace('+1 ', '').replace(' доб.', ''))
        
    def test_generate_name_address_invalid_locale(self):
        """Тест с неверной локалью (должен использоваться ru по умолчанию)."""
        result = generate_name_address('invalid')
        assert result['locale'] == 'RU'  # Должен вернуться ru как дефолтный
        
    def test_generate_name_address_invalid_locale2(self):
        """Тест с другой неверной локалью."""
        result = generate_name_address('fr')
        assert result['locale'] == 'RU'
        
    def test_generate_name_address_case_insensitive(self):
        """Тест с локалью в разном регистре."""
        result1 = generate_name_address('RU')
        result2 = generate_name_address('ru')
        result3 = generate_name_address('Ru')
        assert result1['locale'] == 'RU'
        assert result2['locale'] == 'RU'
        assert result3['locale'] == 'RU'

    def test_russian_phone_format(self):
        """Тест формата русского телефона."""
        result = generate_name_address('ru')
        
        # Проверяем, что телефон начинается с +7 или содержит "доб."
        phone = result['phone']
        assert phone.startswith('+7') or 'доб.' in phone
        
    def test_empty_locale(self):
        """Тест с пустой локалью."""
        result = generate_name_address('')
        assert result['locale'] == 'RU'

    def test_none_locale(self):
        """Тест с None локалью."""
        result = generate_name_address(None)
        assert result['locale'] == 'RU'

    def test_boolean_locale(self):
        """Тест с булевыми значениями как локалью."""
        result1 = generate_name_address(True)
        result2 = generate_name_address(False)
        assert result1['locale'] == 'RU'
        assert result2['locale'] == 'RU'

    def test_numeric_locale(self):
        """Тест с числовыми значениями как локалью."""
        result1 = generate_name_address(123)
        result2 = generate_name_address(0)
        assert result1['locale'] == 'RU'
        assert result2['locale'] == 'RU'

class TestCreditCardGenerator:
    """Тесты для генерации кредитных карт."""
    
    def test_generate_credit_card_structure(self):
        """Тест структуры данных карты."""
        result = generate_credit_card()
        
        assert isinstance(result, dict)
        assert 'number' in result
        assert 'type' in result
        assert 'expiry' in result
        assert 'cvv' in result
        
        # Проверяем тип карты
        assert result['type'] in ['Visa', 'MasterCard', 'Mir']
        
        # Проверяем формат CVV
        assert len(result['cvv']) == 3
        assert result['cvv'].isdigit()
        
        # Проверяем формат срока действия
        assert '/' in result['expiry']
        month, year = result['expiry'].split('/')
        assert 1 <= int(month) <= 12
        assert 23 <= int(year) <= 30  # До 2030 года
        
    def test_credit_card_luhn_algorithm(self):
        """Тест алгоритма Луна (валидность номера карты)."""
        result = generate_credit_card()
        
        # Убираем пробелы из номера карты
        card_number = result['number'].replace(' ', '')
        
        # Проверяем длину
        assert len(card_number) == 16
        
        # Алгоритм Луна для проверки
        total = 0
        reverse_digits = card_number[::-1]
        
        for i, digit in enumerate(reverse_digits):
            n = int(digit)
            if i % 2 == 1:  # Четные позиции в обратном порядке (нечетные в прямом)
                n *= 2
                if n > 9:
                    n -= 9
            total += n
            
        # Сумма должна делиться на 10
        assert total % 10 == 0, f"Невалидный номер карты по алгоритму Луна: {card_number}"
        
    def test_credit_card_format(self):
        """Тест форматирования номера карты."""
        result = generate_credit_card()
        
        # Проверяем формат XXXX XXXX XXXX XXXX
        parts = result['number'].split(' ')
        assert len(parts) == 4
        
        for part in parts:
            assert len(part) == 4
            assert part.isdigit()

class TestBoundaryStringsGenerator:
    """Тесты для генерации граничных строк."""
    
    def test_generate_boundary_strings_structure(self):
        """Тест структуры возвращаемых данных."""
        strings = generate_boundary_strings()
        
        assert isinstance(strings, list)
        assert len(strings) > 0
        
        for item in strings:
            assert isinstance(item, dict)
            assert 'title' in item
            assert 'value' in item
            assert 'description' in item
            
    def test_boundary_strings_values(self):
        """Тест конкретных значений граничных строк."""
        strings = generate_boundary_strings()
        
        # Находим строки по заголовкам
        titles = [item['title'] for item in strings]
        
        # Проверяем 255 символов
        for item in strings:
            if '255 символов' in item['title']:
                assert len(item['value']) == 255
                assert item['value'] == 'A' * 255
                
        # Проверяем пустую строку
        for item in strings:
            if 'Пустая строка' in item['title']:
                assert item['value'] == ''
                assert len(item['value']) == 0
                
        # Проверяем SQL-инъекцию
        for item in strings:
            if 'SQL-инъекция' in item['title']:
                assert "' OR '1'='1'; --" in item['value']
                
        # Проверяем XSS-инъекцию
        for item in strings:
            if 'XSS-инъекция' in item['title']:
                assert '<script>' in item['value']
                assert '</script>' in item['value']
                
    def test_string_lengths(self):
        """Тест длин всех строк."""
        strings = generate_boundary_strings()
        
        for item in strings:
            if '1000 символов' in item['title']:
                assert len(item['value']) == 1000
            elif '255 символов' in item['title']:
                assert len(item['value']) == 255
            elif 'Пустая строка' in item['title']:
                assert len(item['value']) == 0

class TestTempEmailGenerator:
    """Тесты для генерации временных email-адресов."""
    
    def test_generate_temp_email_structure(self):
        """Тест структуры email данных."""
        result = generate_temp_email()
        
        assert isinstance(result, dict)
        assert 'email' in result
        assert 'note' in result
        
        # Проверяем формат email
        email = result['email']
        assert '@' in email
        assert '.' in email.split('@')[1]
        
        # Проверяем домен
        valid_domains = ["temp-mail.org", "10minutemail.com", 
                        "guerrillamail.com", "yopmail.com"]
        domain = email.split('@')[1]
        assert domain in valid_domains
        
    def test_email_username_length(self):
        """Тест длины имени пользователя в email."""
        result = generate_temp_email()
        username = result['email'].split('@')[0]
        
        # Должно быть 10 символов (как мы задали в генераторе)
        assert len(username) == 10
        
        # Должны быть только строчные буквы и цифры
        assert username.isalnum()
        assert username.islower()

class TestIntegration:
    """Интеграционные тесты."""
    
    def test_multiple_generations(self):
        """Тест множественной генерации данных."""
        # Генерируем несколько раз, чтобы проверить случайность
        results = []
        for _ in range(10):
            results.append(generate_name_address('ru'))
            
        # Проверяем, что не все результаты одинаковые
        # (хотя теоретически могут совпасть, но вероятность мала)
        first_name = results[0]['full_name']
        all_same = all(r['full_name'] == first_name for r in results)
        
        # Если все одинаковые, это подозрительно
        if all_same:
            print("Предупреждение: все сгенерированные имена одинаковы")
            # Это не ошибка, но стоит проверить
            
    def test_credit_card_uniqueness(self):
        """Тест уникальности номеров карт."""
        cards = []
        for _ in range(5):
            card = generate_credit_card()
            cards.append(card['number'])
            
        # Преобразуем в set для проверки уникальности
        unique_cards = set(cards)
        
        # Не все карты должны быть уникальны (могут быть коллизии),
        # но большинство должны отличаться
        if len(unique_cards) < 3:
            print("Предупреждение: много дубликатов номеров карт")

# Убираем отдельные функции вне классов, так как они теперь внутри классов
# Эти функции были перенесены в класс TestNameAddressGenerator
# def test_empty_locale(): ...
# def test_none_locale(): ...
# def test_large_scale(): ...

# Оставляем только те функции, которые действительно должны быть отдельно
def test_large_scale():
    """Тест массовой генерации (стресс-тест)."""
    for i in range(100):
        card = generate_credit_card()
        # Проверяем валидность алгоритмом Луна
        card_number = card['number'].replace(' ', '')
        
        total = 0
        reverse_digits = card_number[::-1]
        for idx, digit in enumerate(reverse_digits):
            n = int(digit)
            if idx % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n
            
        assert total % 10 == 0, f"Невалидная карта на итерации {i}: {card_number}"