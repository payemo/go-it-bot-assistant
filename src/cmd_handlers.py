import textwrap
import sys

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum

from prettytable import PrettyTable

from src.assistant import Assistant
from src.fields import Name, Phone, Address, Email, Birthday
from src.tag import Tag

class HandlerResponse:
    class Status(Enum):
        CONTINUE = 1
        FINISH = 2

    def __init__(self, status: Status, msg="") -> None:
        self._msg = msg
        self._status = status

    @property
    def msg(self) -> str:
        return self._msg

    @property
    def status(self) -> Status:
        return self._status


class BaseCommandHandler(ABC):
    def __init__(self, data: Assistant = None) -> None:
        super().__init__()
        self._data = data

    @abstractmethod
    def handle_input(self) -> HandlerResponse:
        return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{self.handle_input.__qualname__}' not implemented.")


class HelpCommandHandler(BaseCommandHandler):
    __commands = {
        'add-record': 'Adds new record. The name and phone are necessary parameters.',
        'edit-record': 'Edit record properties. User should enter the name of the field for editing: name, address, phone, birthday, note',
        'remove-record': 'Remove contact from the address book.',
        'show-all-records': 'Display all existing records.',
        'search-record': 'Search record by a specific criteria: name/phone/email.',
        'add-phone': 'Adds additional phone number for the specified user.',
        'remove-phone': "Remove input phone for the contact from list.",
        'show-upcoming-bdays': 'Output upcoming birthday for the next week.',
        'add-note': 'Adds new note.',
        'edit-note': 'Edit notes title or content.',
        'remove-note': 'Remove note.',
        'show-note': 'Show single note.',
        'show-notes': 'Show all notes.',
        'find-notes-by-date': 'Find notes by period of dates',
        'find-notes-by-word-in-title': 'Find notes by title',
        'find-notes-by-tag': 'Find notes by tag',
        'link-note': 'Links note to the specified record.',
        'create-tag': 'Create new tag.',
        'remove-tag': 'Remove tag.',
        'link-tag': 'Links tag to the specified notes.'
    }

    def handle_input(self) -> HandlerResponse:
        self.__display_commands()
        return HandlerResponse(HandlerResponse.Status.CONTINUE)

    def __display_commands(self) -> None:
        for cmd, description in self.__commands.items():
            print(f"{cmd:<20} - {textwrap.fill(description, width=60, subsequent_indent=' ' * 23)}")


class ExitCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        return HandlerResponse(HandlerResponse.Status.FINISH)


class AddRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            name = Name(input('Enter the name: '))

            if self._data.record_exists(str(name)):
                warn_msg = "Contact already exists."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            phone = Phone(input('Enter the phone: '))

            if self._data.phone_exists(str(phone)):
                warn_msg = f"{phone} already exists in book."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            email = input('Enter the email: ').strip().lower()
            email = Email(email) if email else None

            address = input('Enter the address: ').strip().lower()
            address = Address(address) if address else None

            birthday = input('Enter the birthday (DD.MM.YYYY): ').strip()
            birthday = Birthday(birthday) if birthday else None

            self._data.add_record(name, phone, email, address, birthday)

            return HandlerResponse(HandlerResponse.Status.CONTINUE, "Contat was succesfully added.")

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class EditRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            name = input('Enter contact name to edit: ')

            if not self._data.record_exists(name):
                warn_msg = f"{name} contact does not exist."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            edit_field = input(
                'What field would you like to edit? (Name, Phone, Address, Email, Birthday): ').strip().lower()

            if edit_field == 'phone':
                old_phone = input('Enter phone to edit: ')
                new_phone = input('Enter new phone value: ')

                if self._data.phone_exists(old_phone):
                    self._data.edit_record_phone(name, old_phone, new_phone)
                    return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Edited phone '{old_phone}': '{new_phone}'")
                else:
                    return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{old_phone}' wasn't found.")
            else:
                new_val = input(f"Enter value for the '{edit_field}' field: ").strip()

                match edit_field:
                    case 'name':
                        self._data.edit_record_name(name, new_val)
                    case 'email':
                        self._data.edit_record_email(name, new_val)
                    case 'address':
                        self._data.edit_record_address(name, new_val)
                    case 'birthday':
                        self._data.edit_record_birthday(name, new_val)
                    case _:
                        return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{edit_field} wasn't found.")

                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{edit_field} was successfully edited.")

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class RemoveRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            remove_name = input('Enter the name of a contact to be removed: ')

            if self._data.record_exists(remove_name):
                self._data.remove_record(remove_name)
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{remove_name} was successfully removed.")
            else:
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{remove_name} does not exist.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class ShowAllRecordsCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            table = PrettyTable()
            table.field_names = ["Name", "Phones", "Email", "Address", "Birtday"]

            for rec in self._data.get_records():
                table.add_row([
                    rec.name,
                    "\n".join(str(phone) if phone else '-' for phone in rec.phones),
                    rec.email or '-',
                    rec.address or '-',
                    str(rec.birthday) or '-'
                ])

            print(table)
            return HandlerResponse(HandlerResponse.Status.CONTINUE)
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class SearchRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            search = input('Enter name to search for: ')
            record = self._data.get_record(search)

            table = PrettyTable()
            table.field_names = ["Name", "Phones", "Email", "Address", "Birthday"]

            if record:
                table.add_row([
                    record.name,
                    "\n".join(str(phone) if str(phone) else '-' for phone in record.phones),
                    record.email or '-',
                    record.address or '-',
                    str(record.birthday) or '-'
                ])

            print(table)
            return HandlerResponse(HandlerResponse.Status.CONTINUE)
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class CreateTagCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            tag = input('Enter the tag name: ')

            if self._data.tag_exists(tag):
                warn_msg = "Tag already exists."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            self._data.create_tag(tag)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "Tag was successfully added.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class DeleteTagCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            tag = input('Enter the tag name that should be removed: ')

            if not self._data.tag_exists(tag):
                warn_msg = "Tag does not exists."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            self._data.delete_tag(tag)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "Tag was successfully added.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class ShowAllTagsCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            tag_table = self._data.show_tags()
            if tag_table:
                print(tag_table)
                return HandlerResponse(HandlerResponse.Status.CONTINUE)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "No tags found.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class UnknownRecordCommandHandler(BaseCommandHandler):
    """Handler for catching invalid input commands."""

    def __init__(self, cmd: str) -> None:
        super().__init__()
        self.__cmd = cmd

    def handle_input(self) -> HandlerResponse:
        return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Unknown '{self.__cmd}' input command.")


class AddPhoneCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            name = input('Enter contact name: ')

            if self._data.record_exists(name):
                phone = input('Enter phone: ')

                self._data.add_phone(name, phone)
                return HandlerResponse(HandlerResponse.Status.CONTINUE,
                                       f"'Additional phone {phone}' was added successfully.")
            else:
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{name}' contact not found.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class RemovePhoneCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            name = input('Enter the contact name: ')

            if not self._data.record_exists(name):
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{name} does not exist.")

            phone = input('Enter the phone to be removed: ')

            if not self._data.phone_exists(phone):
                return HandlerResponse(HandlerResponse.Status.CONTINUE,
                                       f"{phone} does not exist in a '{name}' contact book.")

            self._data.remove_phone(name, phone)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{phone} was successfully removed.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class ShowUpcomingBirthdayRecordsCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            table = PrettyTable()
            table.field_names = ["Name", "Congratulation date"]

            for name, bday in self._data.get_records_with_upcoming_birthday():
                table.add_row([name, str(bday)])

            print(table)
            return HandlerResponse(HandlerResponse.Status.CONTINUE)
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class CreateNoteCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            title = input("Enter the title: ")
            if self._data.note_exists(str(title)):
                warn_msg = f"Note with {title} already exists."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            print("Enter/Paste your content. Press Ctrl-D (or Ctrl-Z in Windows) to save it.")
            body = sys.stdin.readlines()
            body = "".join(body).rstrip()

            self._data.add_note(title, body)

            choice = input("Would you like to add any tag? (y/n): ").strip().lower()

            if choice == 'y':
                tag = input('Enter the tag: ')

                if tag:
                    if self._data.tag_exists(tag):
                        self._data.add_tag_to_note(tag)
                    else:
                        create_tag = input(f"Tag '{tag}' does not exist. Would you like to create one? (y/n): ")
                        if create_tag == 'y':
                            self._data.create_tag(tag)
                            self._data.add_tag_to_note(title, tag)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "Note was successfully added.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class FindNotesByDateCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            start_date_str = input("Enter start date to search for notes in format YYYY-MM-DD: ")
            start_date_obj = datetime.strptime(start_date_str, "%Y-%m-%d").date()
            end_date_str = input("Enter end date to search for notes in format YYYY-MM-DD: ")
            end_date_object = datetime.strptime(end_date_str, "%Y-%m-%d").date()
            notes_list = self._data.get_notes_by_period_of_dates(start_date_obj, end_date_object)
            if notes_list:
                table = self._data.create_table_with_notes(notes_list)
                print(table)
                return HandlerResponse(HandlerResponse.Status.CONTINUE)
            return HandlerResponse(
                HandlerResponse.Status.CONTINUE,
                "There are no notes for such date period. Try again with another period.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class FindNotesByTitleCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            word = input("Enter word to search for notes that include it in title: ")
            notes_list = self._data.get_notes_by_word_in_title(word.lower().strip())
            if notes_list:
                table = self._data.create_table_with_notes(notes_list)
                print(table)
                return HandlerResponse(HandlerResponse.Status.CONTINUE)
            return HandlerResponse(
                HandlerResponse.Status.CONTINUE,
                "There are no notes with this word. Try again with another word.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class FindNotesByTagCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            tag = input("Enter tag to search for notes that have it: ")
            notes_list = self._data.get_notes_by_tag(tag.lower().strip())
            if notes_list:
                table = self._data.create_table_with_notes(notes_list)
                print(table)
                return HandlerResponse(HandlerResponse.Status.CONTINUE)
            return HandlerResponse(
                HandlerResponse.Status.CONTINUE,
                "There are no notes with this tag. Try again with another tag.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class LinkNoteToRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            if self._data.get_notes():
                print(self._data.create_table_with_note_titles())

                note_title = input('Enter note to be linked: ')

                # Take into account user's mistakes
                for _ in range(3):
                    if self._data.note_exists(note_title):
                        rec_name = input("Enter contact you wish to link the note: ")

                        if self._data.record_exists(rec_name):
                            # Create new object but keeps tags to be 'movable' for dynamic changes.
                            self._data.link_note_to_record(rec_name, note_title)
                            return HandlerResponse(HandlerResponse.Status, f"Note '{note_title}' was successfull added to the '{rec_name}' contact.")
                        else:
                            print(f'Skip contanct: {rec_name}. Try again ...')
                    else:
                        print(f'Skip note: {note_title}. Try again ...')
            else:
                return HandlerResponse(HandlerResponse.Status, "Note list is empty.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)
        
class ShowRecordNotesCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            name = input('Enter contact name: ')

            if self._data.record_exists(name):
                notes = self._data.get_record_notes(name)

                if notes:
                    print(self._data.create_table_with_notes(notes))
                    return HandlerResponse(HandlerResponse.Status.CONTINUE)
                else:
                    return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Contact '{name}' has no any note.")
            return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Contact '{name}' does not exist.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class EditNoteCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            title = input('Choose title to edit: ')

            if not self._data.note_exists(title):
                warn_msg = (f"{title} note does not exist. "
                            f"Try to find a correct title with another command,"
                            f"like find-notes-by-date or find-notes-by-word-in-title.")
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            edit_field = input(
                'What field would you like to edit? (Title, Content): ').strip().lower()

            new_val = input(f"Enter value for the '{edit_field}' field: ").strip()

            match edit_field:
                case 'title':
                    self._data.edit_notes_title(title, new_val)
                case 'content':
                    self._data.edit_notes_content(title, new_val)
                case _:
                    return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{edit_field} wasn't found.")

            return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{edit_field} was successfully edited.")

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class RemoveNoteCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            remove_title = input('Enter the title of a note to be removed: ')

            if self._data.note_exists(remove_title):
                self._data.remove_note(remove_title)
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{remove_title} was successfully removed.")
            return HandlerResponse(HandlerResponse.Status.CONTINUE, f"{remove_title} does not exist.")

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class LinkTagToNotesCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            tag = input('Enter tag name: ')

            if self._data.tag_exists(tag):
                print("Enter notes you'd like tag to be linked. Press Ctrl-D (or Ctrl-Z in Windows) to save it.")
                notes = [line.strip() for line in sys.stdin]

                for note_title in notes:
                    note = self._data.get_note(note_title)
                    if note:
                        if self._data.get_notes_by_tag(tag):
                            print(f"'{tag}' already linked.")
                        else:
                            self._data.add_tag_to_note(note_title, tag)
                    else:
                        print(f"'{note}' skipped.")
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Tag '{tag}' was successfully linked to the specified notes.")
            else:
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{tag}' does not exist.")
        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)

class DisplayNoteCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            if not self._data.get_notes():
                return HandlerResponse(HandlerResponse.Status.CONTINUE, "There are no notes in notebook.")
            else:
                print(self._data.create_table_with_note_titles())

            title = input('Choose title from the table above: ')

            if not self._data.note_exists(title):
                warn_msg = f"{title} note does not exist. "
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            note = self._data.get_note(title)
            table = self._data.create_table_with_notes([note])
            print(table)
            return HandlerResponse(HandlerResponse.Status.CONTINUE)

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)


class DisplayAllNotesCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        try:
            notes = self._data.get_notes()
            if notes:
                table = self._data.create_table_with_notes(notes)
                print(table)
                return HandlerResponse(HandlerResponse.Status.CONTINUE)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "There are no notes in the notebook.")

        except Exception as e:
            return HandlerResponse(HandlerResponse.Status.CONTINUE, e)
