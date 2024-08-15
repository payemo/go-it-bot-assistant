from typing import List
from src.fields import Name, Address, Phone, Email, Birthday

class Record:
    def __init__(self, name: Name, phone: Phone, email: Email = None, address: Address = None, bday: Birthday = None) -> None:
        self._name = name
        self._address = address
        self._email = email
        self._birthday = bday
        self._phones = [phone]

    @property
    def phones(self):
        return self._phones
    
    def __str__(self) -> str:
        return f"{self._name}:{self._email}"
