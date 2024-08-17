from typing import Dict, List, Generator, Tuple
from datetime import datetime, timedelta, date

from prettytable import PrettyTable

from src import Note
from src.record import Record
from src.fields import Name, Phone, Address, Email, Birthday
from src.tag import Tag


class Assistant:
    def __init__(self) -> None:
        self._records = {}
        self._notes = {}
        self._tags = {}

    def record_exists(self, name: str) -> bool:
        if self._records.get(name):
            return True
        return False

    def phone_exists(self, phone: str) -> bool:
        return any(str(p) == phone for rec in self._records.values() for p in rec.phones)

    def tag_exists(self, name: str) -> bool:
        if self._tags.get(name):
            return True
        return False

    def add_record(self, name: Name, phone: Phone, email: Email = None, address: Address = None,
                   birthday: Birthday = None) -> None:
        self._records[str(name)] = Record(name, phone, email, address, birthday)

    def edit_record_phone(self, rec_name: str, old_phone: str, new_phone: str) -> None:
        rec = self._records[rec_name]

        for idx, phone in enumerate(rec.phones):
            if str(phone) == old_phone:
                rec.phones[idx] = Phone(new_phone)

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
        self._records[name].phones.append(Phone(phone))

    def remove_phone(self, name: str, phone: str) -> None:
        self._records[name].phones = [p for p in self._records[name].phones if p.value != phone]

    def get_records_with_upcoming_birthday(self) -> Generator[Tuple[str, date], None, None]:
        today = datetime.now().date()
        end_date = today + timedelta(days=7)

        for rec in self._records.values():
            if rec.birthday:
                user_bday = rec.birthday
                bday_this_year = user_bday.replace(year=today.year)

                if today <= bday_this_year <= end_date:
                    if bday_this_year.weekday() == 5:  # Saturday
                        bday_this_year += timedelta(days=2)
                    elif bday_this_year.weekday() == 6:  # Sunday
                        bday_this_year += timedelta(days=1)

                    yield rec.name, bday_this_year

    def note_exists(self, title: str) -> bool:
        if self._notes.get(title):
            return True
        return False

    def add_note(self, title, content) -> None:
        note = Note(title=title, content=content)
        note.created_at = datetime.now()
        self._notes[title] = note

    def add_tag_to_note(self, note_title: str, tag_name: str) -> None:
        note = self._notes[note_title]
        note.tags.append(self._tags[tag_name])

    def edit_notes_title(self, title: str, new_title: str) -> None:
        self._notes[new_title] = self._notes.pop(title)
        self._notes[new_title].modified_at = datetime.now()

    def edit_notes_content(self, title: str, new_content: str) -> None:
        note = self._notes[title]
        note.content = note.format_note(new_content)
        note.modified_at = datetime.now()

    def remove_note(self, title: str) -> None:
        del self._notes[title]

    def get_note(self, title: str) -> Note:
        return self._notes.get(title)

    def get_notes(self) -> List[Note]:
        return self._notes.values()

    def get_notes_by_period_of_dates(self, start_date: date, end_date: date) -> List[Note]:
        notes = []
        for note in self._notes.values():
            if start_date <= note.created_at.date() <= end_date:
                notes.append(note)
        return notes

    def get_notes_by_word_in_title(self, word: str) -> List[Note]:
        notes = []
        for note in self._notes.values():
            if word in note.title:
                notes.append(note)
        return notes

    def get_notes_by_tag(self, tag: str) -> List[Note]:
        notes = []
        for note in self._notes.values():
            if tag in note.tags:
                notes.append(note)
        return notes

    @staticmethod
    def create_table_with_notes(notes_list: List[Note]) -> PrettyTable:
        table = PrettyTable()
        table.field_names = ["Title", "Content", "Tags", "Created", "Last edit"]

        for note in notes_list:
            table.add_row([
                note.title,
                note.content,
                ",".join(note.tags),
                note.created_at.strftime('%Y-%m-%d %H:%M') or '-',
                (
                    note.modified_at.strftime('%Y-%m-%d %H:%M')
                    if note.modified_at
                    else '-'
                ),
            ])
        return table

    def create_table_with_note_titles(self) -> PrettyTable | None:
        titles = [note.title for note in self._notes.values()]
        if titles:
            title_table = PrettyTable()
            title_table.field_names = ["All notes titles"]
            for title in titles:
                title_table.add_row([title])
            return title_table
        return None

    def create_tag(self, name: str) -> None:
        self._tags[name] = Tag(name)

    def delete_tag(self, name: str) -> None:
        for note in self._notes.values():
            if self._tags[name] in note.tags:
                note.tags.remove(self._tags[name])
        del self._tags[name]

    def show_tags(self) -> PrettyTable | None:
        if not self._tags:
            return None

        if self._tags:
            tag_table = PrettyTable()
            tag_table.field_names = ["All tags"]
            for tag in self._tags.values():
                tag_table.add_row([str(tag.name)])
            return tag_table
