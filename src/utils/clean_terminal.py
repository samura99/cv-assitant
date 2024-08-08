import os

def clean():
    if os.name == 'nt':  # Para Windows
        _ = os.system('cls')
    else:  # Para Unix/Linux
        _ = os.system('clear')