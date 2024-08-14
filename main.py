from src.cmd_parser import CommandParser
from src.cmd_handlers import HandlerResponse

def main():
    while True:
        cmd = input('Enter the command (use \'help\' to list all available commands): ')
        response = CommandParser.parse(cmd).handle_input()

        if response.err_msg:
            print(response.err_msg)

        if response.status == HandlerResponse.Status.FINISH:
            break

if __name__ == '__main__':
    main()