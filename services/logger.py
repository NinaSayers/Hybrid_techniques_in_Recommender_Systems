from datetime import datetime
from colorama import Fore, Style, init
from IPython.display import display, Markdown
import io

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
    
    def print_markdown_table(self, headers, rows):
        # Create table in Markdown format
        markdown_table = "| " + " | ".join(headers) + " |\n"
        markdown_table += "|---" * len(headers) + "|\n"
        for row in rows:
            markdown_table += "| " + " | ".join(str(cell) for cell in row) + " |\n"
        
        # Print the Markdown table
        # Use a file-like object to capture Markdown output in a Jupyter notebook
        buf = io.StringIO()
        buf.write(markdown_table)
        buf.seek(0)
        markdown_output = buf.getvalue()
        display(Markdown(markdown_output))
