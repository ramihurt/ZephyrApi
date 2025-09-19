from WMessageEmitter import MessageEmitter
from colorama import init, Fore

init()

class MessageSender:
    def __init__(self, emitter: MessageEmitter):
        self.emitter = emitter

    def send_message(self, message:str):
        """ Prints message black on frontend and white on backend terminal"""
        colored_message = {"text": message, "color": "#000000"}  # Black for white background on frontend
        print(f"{Fore.WHITE}{message}{Fore.RESET}")  # White for black terminal
        self.emitter.emit(colored_message)

    def send_green_message(self, message:str):
        """ Prints message green on frontend and green on backend terminal"""
        colored_message = { "text": message, "color":"#00bf0c" }
        print(f"{Fore.GREEN}{message}{Fore.RESET}")
        self.emitter.emit(colored_message)

    def send_warning(self, message:str):
        """ Prints warning message orange on frontend and yellow on backend terminal"""
        colored_message = { "text": message, "color":"#ffc80d"} # Orange
        print(f"{Fore.YELLOW}{message}{Fore.RESET}")
        self.emitter.emit(colored_message)

    def send_error(self, message:str):
        """ Prints error message red on frontend and red on backend terminal"""
        colored_message = { "text": message, "color": "#df0000"} # Red
        print(f"{Fore.RED}{message}{Fore.RESET}")
        self.emitter.emit(colored_message)