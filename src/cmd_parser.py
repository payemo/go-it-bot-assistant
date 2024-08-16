import src.cmd_handlers as handlers
from src.exceptions import UnknownInputCommand
from src.assistant import Assistant

class CommandParser:
    """Factory method for input commands."""

    @staticmethod
    def parse(cmd: str, data: Assistant) -> handlers.BaseCommandHandler:
        match cmd:
            case 'help':
                return handlers.HelpCommandHandler(data)
            case 'add-record':
                return handlers.AddRecordCommandHandler(data)
            case 'create-tag':
                return handlers.CreateTagCommandHandler(data)
            case 'edit-record':
                return handlers.EditRecordCommandHandler(data)
            case 'show-record':
                return handlers.SearchRecordCommandHandler(data)
            case 'exit' | 'close':
                return handlers.ExitCommandHandler(data)
            case _:
                return handlers.UnknownRecordCommandHandler(cmd)