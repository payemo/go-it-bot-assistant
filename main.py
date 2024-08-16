import sys

from src.cmd_parser import CommandParser
from src.cmd_handlers import HandlerResponse
from src.data_manager import DataManager
from src.picture import StartupPicture


def main():
    StartupPicture.print_picture()
    dm = DataManager()
    data = dm.load_data()

    while True:
        cmd = input('Enter the command (use \'help\' to list all available commands): ')
        response = CommandParser.parse(cmd, data).handle_input()

        if response.msg:
            print(response.msg)

        if response.status == HandlerResponse.Status.FINISH:
            break
    
    dm.save_data(data)

if __name__ == '__main__':
    main()