import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
settings = fl.Folder(os.path.join(cwd, "Settings"))

def main():
    while True:
        # Print all settings
        print("Current settings: ")
        [print(fl.CFG(os.path.join(settings.path, setting + ".cfg"))) for setting in cs.settings]
        
        # Print setting selection screen
        print()
        for setting, x in zip(cs.settings, range(len(cs.settings))):
            print(chr(x + 65), ". ", setting, sep = "")
        print("X. Exit the menu")
        
        setting = str(input("Which setting should be edited? (Enter the corresponding letter): ")).upper()
        
        match setting:
            case "A":
                cfg = fl.CFG(os.path.join(settings.path, "directory.cfg"))
                drive = os.path.splitdrive(os.getcwd())[0]
                print("The current value is:", cfg.get_value())
                print(f"Enter the directory where the files should be moved to after patching, separated by the {os.sep} character.")
                print("Do not include the drive name. Start with the first folder of your directory.")
                print(f"For example, the directory {drive}{os.sep}Users{os.sep}admin{os.sep}Documents would be entered as Users{os.sep}admin{os.sep}Documents.")
                
                while True:
                    folders = str(input("Directory: ")).split(os.sep)
                    
                    
                    directory = drive + os.sep
                    for folder in folders:
                        directory = os.path.join(directory, folder)
                    
                    if os.path.exists(directory):
                        break
                    else:
                        print("This directory does not exist. Please try again.")
                
                cfg.set_value(directory)
                ft.clear_screen()
            case "B":
                cfg = fl.CFG(os.path.join(settings.path, "iso-rename.cfg"))
                print("The current value is:", cfg.get_value())
                iso_rename = ft.question("Rename an ISO after patching?")
                
                cfg.set_value(iso_rename)
                ft.clear_screen()
            case "C":
                cfg = fl.CFG(os.path.join(settings.path, "perf-monitor.cfg"))
                print("The current value is:", cfg.get_value())
                perf_monitor = ft.question("Enable the performance monitor?")
                
                cfg.set_value(perf_monitor)
                ft.clear_screen()
            case "D":
                cfg = fl.CFG(os.path.join(settings.path, "pref-language.cfg"))
                print("The current value is:", cfg.get_value())
                
                for identifier in cs.identifiers:
                    print(identifier, ". ", cs.languages[cs.identifiers.index(identifier)], sep = "")
                
                while True:
                    pref_language = str(input("What is your preferred language? (Enter the correct identifier): ")).upper()
                    
                    if pref_language in cs.identifiers:
                        break
                    else:
                        print("This is not an option. Please try again.")
                
                cfg.set_value(pref_language)
                ft.clear_screen()
            case "E":
                cfg = fl.CFG(os.path.join(settings.path, "pycache.cfg"))
                print("The current value is:", cfg.get_value())
                delete_pycache = ft.question("Delete the \"__pycache__\" folder after patching?")
    
                cfg.set_value(delete_pycache)
                ft.clear_screen()
            case "F":
                cfg = fl.CFG(os.path.join(settings.path, "riivo-suffix.cfg"))
                print("The current value is:", cfg.get_value())
                riivo_suffix = ft.question("Add a suffix to Riivolution builds after patching?")
                
                cfg.set_value(riivo_suffix)
                ft.clear_screen()
            case "X":
                break
            case _:
                print("This is not an option. Please try again.")
    
    input("All done!")

if __name__ == "__main__":
    main()
