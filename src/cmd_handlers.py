import textwrap
from abc import ABC, abstractmethod
from enum import Enum
from functools import wraps
from typing import Callable

class HandlerResponse:
    class Status(Enum):
        CONTINUE = 1
        FINISH = 2

    def __init__(self, status: Status, err_msg="") -> None:
        self._err_msg = err_msg
        self._status = status

    @property
    def err_msg(self) -> str:
        return self._err_msg
    
    @property
    def status(self) -> Status:
        return self._status

def catch_handler_error(func: Callable) -> Callable:
    @wraps(func)
    def inner() -> HandlerResponse:
        try:
            return func()
        except Exception as e:
            return str(e)
    return inner

class BaseCommandHandler(ABC):
    @abstractmethod
    #@catch_handler_error
    def handle_input(self) -> HandlerResponse:
        return HandlerResponse(HandlerResponse.Status.CONTINUE, f"'{self.handle_input.__qualname__}' not implemented.")

class HelpCommandHandler(BaseCommandHandler):
    __commands = {
        'add-record': 'Adds new record. The name and phone are necessary parameters.',
        'edit-record': 'Edit record properties. User should enter the name of the field for editing: name, address, phone, birthday, note',
        'remove-record': 'Remove contact from the address book.',
        'show-all-records': 'Display all existing records.',
        'search-record': 'Search record by a specific criteria: name/phone/email.',
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
        pass

class EditRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        pass

class RemoveRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        pass

class ShowAllRecordsCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        pass

class SearchRecordCommandHandler(BaseCommandHandler):
    def handle_input(self) -> HandlerResponse:
        pass

class UnknownRecordCommandHandler(BaseCommandHandler):
    """Handler for catching invalid input commands."""
    def __init__(self, cmd: str) -> None:
        super().__init__()
        self.__cmd = cmd

    def handle_input(self) -> HandlerResponse:
        return HandlerResponse(HandlerResponse.Status.CONTINUE, f"Unknown '{self.__cmd}' input command.")