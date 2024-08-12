from src.commands import CmdFactory, ProgramStatus
from src.record import AddressBookManager

def main():
    addr_book_manager = AddressBookManager()
    addr_book_manager.init_data()

    try:
        while CmdFactory.get().invoke(addr_book_manager) != ProgramStatus.FINISH:
            pass
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()