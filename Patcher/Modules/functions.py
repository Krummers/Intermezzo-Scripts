import os
import platform as pf
import requests as rq

import Modules.constants as cs

def download(link, path):
    data = rq.get(link)
    
    with open(path, "wb") as file:
        file.write(data.content)

def question(string):
    while True:
        choice = str(input(string + " (Y or N): ")).lower()
        
        if choice in cs.binaries[:2]:
            return True
        elif choice in cs.binaries[2:]:
            return False
        else:
            print("This is not an option. Please try again.")

def drive_selection():
    if pf.uname()[0] == "Windows":
        drives = []
        for letter in [chr(x) for x in range(65, 65 + 26)]:
            if os.path.exists(f"{letter}:"):
                drives.append(letter)
        
        for letter in drives:
            print(f"{letter}. Drive {letter}:")
        
        while True:
            choice = str(input("Which drive should be used? (Enter the corresponding option): ")).upper()
            
            if choice in drives:
                return f"{choice}:"
            else:
                print("This is not an option. Please try again.")
    else:
        return ""

def clear_screen():
    if pf.uname()[0] == "Windows":
        os.system("cls")
    else:
        os.system("clear")
