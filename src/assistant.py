from typing import Dict, List
from src.record import Record
from src.fields import Name, Phone, Address, Email, Birthday
from src.tag import Tag


class Assistant:
    def __init__(self) -> None:
        self._records = {}
        self._tags = {}
        self._notes = {}

    def record_exists(self, name: str) -> bool:
        if self._records.get(name):
            return True
        return False
    
    def phone_exists(self, phone: str) -> bool:
        return any(str(p) == phone for rec in self._records.values() for p in rec.phones)
    
    def add_tag(self, name: str) -> None:
        self._tags[name] = Tag(name)

    def tag_exists(self, name: str) -> bool:
        if self._tags.get(name):
            return True
        return False

    def add_record(self, name: Name, phone: Phone, email: Email = None, address: Address = None, birthday: Birthday = None) -> None:
        self._records[str(name)] = Record(name, phone, email, address, birthday)

    def edit_record_phone(self, rec_name: str, old_phone: str, new_phone: str) -> None:
        rec = self._records[rec_name]

        for phone in rec.phones:
            if old_phone == str(phone):
                phone = Phone(new_phone)

    def edit_record_email(self, rec_name: str, new_value: str) -> None:
        rec = self._records[rec_name]
        rec.email = new_value

    def edit_record_address(self, rec_name: str, new_value: str) -> None:
        rec = self._records[rec_name]
        rec.address = new_value

    def edit_record_birthday(self, rec_name: str, new_value: str) -> None:
        rec = self._records[rec_name]
        rec.birthday = new_value

    def edit_record_name(self, rec_name: str, new_value: str) -> None:
        rec = self._records[rec_name]
        rec.name = new_value

    def remove_record(self, rec_name: str) -> None:
        del self._records[rec_name]

    def get_record(self, name: str) -> Record:
        return self._records.get(name)
    
    def get_records(self) -> List[Record]:
        return self._records.values()
    
    def add_phone(self, name: str, phone: str) -> None:
        self._records[name].append_phone(phone)
