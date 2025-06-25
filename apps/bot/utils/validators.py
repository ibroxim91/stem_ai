import re
from aiogram.exceptions import TelegramBadRequest

VALID_PHONE_CODES = ['90', '91', '93', '94', '95', '97', '98', '99', '88', '33']

def validate_fullname(name: str) -> bool:
    return len(name.strip()) >= 3

def validate_surname(name: str) -> bool:
    return len(name.strip()) >= 5

def validate_phone(phone: str) -> bool:
    pattern = r'^\+998(' + '|'.join(VALID_PHONE_CODES) + r')\d{7}$'
    return re.fullmatch(pattern, phone) is not None

def validate_age(age: str) -> bool:
    if not age.isdigit():
        return False
    age = int(age)
    return 7 <= age <= 100
