import src.cmd_handlers as handlers
from src.exceptions import UnknownInputCommand

class CommandParser:
    """Factory method for input commands."""

    @staticmethod
    def parse(cmd: str) -> handlers.BaseCommandHandler:
        match cmd:
            case 'help':
                return handlers.HelpCommandHandler()
            case 'exit':
                return handlers.ExitCommandHandler()
            case _:
                return handlers.UnknownRecordCommandHandler(cmd)