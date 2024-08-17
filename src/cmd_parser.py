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
            case 'edit-record':
                return handlers.EditRecordCommandHandler(data)
            case 'remove-record':
                return handlers.RemoveRecordCommandHandler(data)
            case 'show-record':
                return handlers.SearchRecordCommandHandler(data)
            case 'show-all-records':
                return handlers.ShowAllRecordsCommandHandler(data)
            case 'add-phone':
                return handlers.AddPhoneCommandHandler(data)
            case 'remove-phone':
                return handlers.RemovePhoneCommandHandler(data)
            case 'show-upcoming-bdays':
                return handlers.ShowUpcomingBirthdayRecordsCommandHandler(data)
            case 'add-tag':
                return handlers.CreateTagCommandHandler(data)
            case 'add-note':
                return handlers.CreateNoteCommandHandler(data)
            case 'edit-note':
                return handlers.EditNoteCommandHandler(data)
            case 'remove-note':
                return handlers.RemoveNoteCommandHandler(data)
            case 'show-note':
                return handlers.DisplayNoteCommandHandler(data)
            case 'show-notes':
                return handlers.DisplayNotesCommandHandler(data)
            case 'exit' | 'close':
                return handlers.ExitCommandHandler(data)
            case _:
                return handlers.UnknownRecordCommandHandler(cmd)