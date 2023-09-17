import os
import platform as pf
import requests as rq
import win32api as wa

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
        choices = []
        options = []
        for drive in wa.GetLogicalDriveStrings().split("\000")[:-1]:
            choices.append(drive[:-2])
            options.append(drive[:-1])
        
        for x in range(len(options)):
            print(f"{choices[x]}. Drive {options[x]}")
        
        while True:
            choice = str(input("Which drive should be used? (Enter the corresponding option): ")).upper()
            
            if choice in choices:
                return options[choices.index(choice)]
            else:
                print("This is not an option. Please try again.")
    else:
        return ""

def clear_screen():
    if pf.uname()[0] == "Windows":
        os.system("cls")
    else:
        os.system("clear")
