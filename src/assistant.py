from typing import Dict
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
    
    def phone_exists(self, phone: Phone) -> bool:
        return any([[rec_phone == phone for rec_phone in rec.phones] for rec in self._records.values()])
    
    def add_record(self, name: Name, phone: Phone) -> None:
        self._records[str(name)] = Record(name, phone)

    def add_tag(self, name: str) -> None:
        self._tags[name] = Tag(name)

    def tag_exists(self, name: str) -> bool:
        if self._tags.get(name):
            return True
        return False