from typing import List
from datetime import date
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
    
    @phones.setter
    def phones(self, value: List[Phone]):
        self._phones = value
    
    @property
    def name(self) -> str:
        return self._name.value if self._name else ''
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = Name(value) if value else None

    @property
    def address(self) -> str:
        return self._address.value if self._address else ''
    
    @address.setter
    def address(self, value: str):
        self._address = Address(value) if value else None

    @property
    def email(self) -> str:
        return self._email.value if self._email else ''
    
    @email.setter
    def email(self, value: str) -> None:
        self._email = Email(value) if value else None

    @property
    def birthday(self) -> date:
        return self._birthday.value if self._birthday else None
    
    @birthday.setter
    def birthday(self, value: str) -> None:
        self._birthday = Birthday(value) if value else None
    
    def __str__(self) -> str:
        return f"{self._name}:{self._email}"
