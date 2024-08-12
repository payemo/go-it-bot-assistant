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

        try:
            addr_book_manager.add_record(name, phone)
        except:
            raise

class AddPhoneCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        name = input('Enter name: ').strip().lower()
        phone = input('Enter additional phone: ').strip().lower()

        try:
            addr_book_manager.add_phone(name, phone)
        except:
            raise

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


class EditRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class RemoveRecordCommand(BaseCommand):
    def invoke(self, addr_book_manager: AddressBookManager) -> ProgramStatus:
        pass

class DisplayRecordsCommand(BaseCommand):
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
            case "add-record":
                return AddRecordCommand()
            case "add-phone":
                return AddPhoneCommand()
            case "search-record":
                return SeachRecordCommand()
            case "edit-record":
                return EditRecordCommand()
            case "remove-record":
                return RemoveRecordCommand()
            case "display-records":
                return DisplayRecordsCommand()
            case "exit" | "stop":
                return StopProgramCommand()
            case _:
                raise CommandNotSpecified(f"Command [{'?' if not user_input else user_input}] not found.")
