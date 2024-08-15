from typing import List
import pickle
from collections import UserDict
from .fields import Name, Address, Phone, Email, Birthday

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
        return f"{self._name}, {'-' if not self._address else self._address}, {'-' if not self._email else self._email}, {'-' if not self._birthday else self._birthday}, {";".join(str(p) for p in self._phones)}"

class AddressBook(UserDict):
    pass

class AddressBookManager:
    def __init__(self, filename: str = "address_book.pkl") -> None:
        self._address_book: AddressBook = None
        self._filename = filename

    def init_data(self):
        try:
            with open(self._filename, 'rb') as file:
                self._address_book = pickle.load(file)
        except FileNotFoundError:
            self._address_book = AddressBook()

    def save_data(self):
        with open(self._filename, 'wb') as file:
            pickle.dump(self._address_book, file)

    def add_record(self, name: str, phone: str, email: str, address: str, birthday: str) -> None:
        new_record = Record(Name(name), Phone(phone), Email(email), Address(address), Birthday(birthday))
        
        if name not in self._address_book:
            self._address_book[name] = new_record

    def edit_record(self, name: str, phone: str) -> None:
        if name not in self._address_book:
            raise
        record = self._address_book.get(name)
        record.phones.append(Phone(phone))

    def show_records(self) -> Record:
        result = "List of stored contacts:"
        for name, record in self._address_book:
            result += f"\n\r{record}"
            print(f"{result}")
        return result
