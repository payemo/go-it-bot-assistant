from typing import List
from collections import UserDict

class Field:
    def __init__(self, value) -> None:
        self._validate(value)
        self._value = value

    def __str__(self) -> str:
        return str(self._value)
    
    def _validate(self, value: str):
        raise NotImplementedError(f"[Field.{self._validate.__name__}] not implemented.")
    
class Name(Field):
    def _validate(self, value: str):
        pass
    
class Phone(Field):
    def _validate(self, value: str):
        pass

class Address(Field):
    def _validate(self, value: str):
        pass

class Email(Field):
    def _validate(self, value: str):
        pass

class Birthday(Field):
    def _validate(self, value: str):
        pass

class Record:
    def __init__(self, name: Name, phone: Phone, email: Email = None, address: Address = None, bday: Birthday = None) -> None:
        self._name = name
        self._address = address
        self._email = email
        self._birthday = bday
        self._phones = [phone]
        self._notes = [None]

        @property
        def notes(self) -> List[Note]:
            return self._notes


class AddressBook(UserDict):
    pass

class Tag:
    def __init__(self, name: str) -> None:
        self._name = name
        
    def __str__(self) -> str:
        return str(self._name)
    
    @property
    def name(self) -> str:
        return self._name
    
    @name.setter
    def name(self, value: str) -> None:
        self._name = value

class Note:
    def __init__(self, text: str, tags: List[str] = [None]) -> None:
        self._text = text
        self._tags = [Tag(tag_name) for tag_name in tags]

class NoteSearchEngine:

    @staticmethod
    def search_by_name(book: AddressBook, name: str) -> List[Note]:
        return book[name].notes
    
    @staticmethod
    def search_by_tag(book: AddressBook, search_tags: List[str]) -> List[Note]:
        out_notes = []
        for _, record in book:
            for note in record.notes:
                for tag in note.tags:
                    if str(tag) in search_tags:
                        out_notes.append(note)
        return out_notes