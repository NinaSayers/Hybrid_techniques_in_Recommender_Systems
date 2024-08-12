from datetime import datetime

class Logger:
    '''Basic logger, with hope to be changed some day'''
    def info(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'[INFO] {current_time}: {log}')
    
    def error(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'[ERROR] {current_time}: {log}')
    
    def warn(self, log): 
        current_time = datetime.now().strftime('%H:%M:%S')
        print(f'[WARN] {current_time}: {log}')
