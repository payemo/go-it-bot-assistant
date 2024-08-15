from src.cmd_parser import CommandParser
from src.cmd_handlers import HandlerResponse
from src.data_manager import DataManager

def main():
    #dm = DataManager()
    #data = dm.load_data()

    while True:
        cmd = input('Enter the command (use \'help\' to list all available commands): ')
        response = CommandParser.parse(cmd).handle_input()

        if response.err_msg:
            print(response.err_msg)

        if response.status == HandlerResponse.Status.FINISH:
            break
    
    #dm.save_data(data)

if __name__ == '__main__':
    main()