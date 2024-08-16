import textwrap
from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from typing import Callable

from src.assistant import Assistant
from src.fields import Name, Phone, Address, Email, Birthday
from src.tag import Tag


from prettytable import PrettyTable

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
        'create-tag': 'Create new tag.',
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

            if self._data.record_exists(name):
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
            
            edit_field = input('What field would you like to edit? (Name, Phone, Address, Email, Birthday): ').strip().lower()

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
            remove_name = input('Enter the name of a contact to be remove: ')

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
            table.field_names = ["Name", "Phones", "Email", "Address", "Birtday"]
            
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
            tag = Tag(input('Enter the tag name: '))

            if self._data.tag_exists(tag):
                warn_msg = "Tag already exists."
                return HandlerResponse(HandlerResponse.Status.CONTINUE, warn_msg)

            self._data.add_tag(tag)
            return HandlerResponse(HandlerResponse.Status.CONTINUE, "Tag was successfully added.")
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
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'Additional phone {phone}' was added successfully.")
            else:
                return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{name}' contact not found.")
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
