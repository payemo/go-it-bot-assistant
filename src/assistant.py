from enum import Enum
from .exceptions import CommandNotSpecified
from .record import AddressBookManager

from prettytable import PrettyTable

table = PrettyTable(field_names=["Name, Address, Email, Birthday, Phones"], print_empty=True)

class ProgramStatus(Enum):
    FINISH = 1
    ACTIVE = 2
    ERROR = 3

class BaseCommand:
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        raise NotImplementedError(f"[BaseCommand.{self.invoke.__name__}] not implemented")
    
class AddRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        name = input('Enter name: ').strip().lower()
        phone = input('Enter phone: ').strip().lower()
        email = input('Enter email: ').strip().lower()
        address = input('Enter address: ').strip().lower()
        birthday = input('Enter birthday: ').strip().lower()

        try:
            addr_book_manager.add_record(name=name, phone=phone,email=email,address=address,birthday=birthday)
        except:
            raise

class EditRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class RemoveRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class ShowRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        print(f"{addr_book_manager.show_records}")

class ShowRecordsCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class SeachRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        criteria = input('Enter search criteria (name/address/phone/email/birthday): ')
        
        match criteria:
            case 'name':
                name = input('Enter name to look for: ')
                record = addr_book_manager.search_by_name(name)
                rec_str = [v for v in str(record).split(',')]
                table.add_row(rec_str)
                print(table)

class BirthdayRecordsCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class AddTagCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class EditTagCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
            pass

class AddNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass
class EditNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class ShowNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
            pass

class ShowNotesCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class SearchNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class DeleteNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class LinkNoteCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class StopProgramCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        addr_book_manager.save_data()
        return ProgramStatus.FINISH

class CmdFactory:

    @staticmethod
    def get() -> BaseCommand:
        user_input = input('Enter the command: ')

        match user_input:
            case "add-contact":
                return AddRecordCommand()
            case "edit-contact":
                return EditRecordCommand()
            case "remove-contact":
                return RemoveRecordCommand()
            case "show-contact":
                return ShowRecordCommand()
            case "show-contacts":
                return ShowRecordsCommand()
            case "search-contact":
                return SeachRecordCommand()
            case "birthdays":
                return BirthdayRecordsCommand()
            case "add_tag":
                return AddTagCommand()
            case "edit_tag":
                return EditTagCommand()
            case "add-note":
                return AddNoteCommand()
            case "edit-note":
                return EditNoteCommand()
            case "show-note":
                return ShowNoteCommand()
            case "show-notes":
                return ShowNotesCommand()
            case "search-note":
                return SearchNoteCommand()
            case "link-note":
                return LinkNoteCommand()
            case "delete-note":
                return DeleteNoteCommand()
            case "exit" | "stop":
                return StopProgramCommand()
            case _:
                raise CommandNotSpecified(f"Command [{'?' if not user_input else user_input}] not found.")
