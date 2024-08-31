from datetime import datetime
from colorama import Fore, Style, init

# Inicializar colorama (importante para Windows)
init(autoreset=True)

class Logger:
    '''Basic logger with color output'''
    
    def info(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'{Fore.GREEN}[INFO] {current_time}: {log}{Style.RESET_ALL}')
    
    def error(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'{Fore.RED}[ERROR] {current_time}: {log}{Style.RESET_ALL}')
    
    def warn(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'{Fore.YELLOW}[WARN] {current_time}: {log}{Style.RESET_ALL}')
