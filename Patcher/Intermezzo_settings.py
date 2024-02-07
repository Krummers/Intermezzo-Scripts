import os

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
settings = fl.Folder(os.path.join(cwd, "Settings"))

def main():
    while True:
        
        # Print setting selection screen
        print("Current settings: ")
        for setting, x in zip(cs.settings, range(len(cs.settings))):
            print(f"{chr(x + 65)}. {fl.CFG(os.path.join(settings.path, setting + '.cfg'))}")
        print("S. Set default settings")
        print("X. Exit the menu")
        
        setting = str(input("Which setting should be edited? (Enter the corresponding letter): ")).upper()
        
        match setting:
            case "A":
                cfg = fl.CFG(os.path.join(settings.path, "directory.cfg"))
                print("The current value is:", cfg.get_value())
                print("This directory is the location the new build gets moved to after the patcher has finished.")
                drive = ft.drive_selection()
                print(f"Enter the directory separated by the {os.sep} character.")
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
                cfg = fl.CFG(os.path.join(settings.path, "downloads.cfg"))
                print("The current value is:", cfg.get_value())
                print("This directory is the folder that gets checked for recently downloaded patch2.tar.")
                drive = ft.drive_selection()
                print(f"Enter the directory separated by the {os.sep} character.")
                print("Do not include the drive name. Start with the first folder of your directory.")
                print(f"For example, the directory {drive}{os.sep}Users{os.sep}admin{os.sep}Downloads would be entered as Users{os.sep}admin{os.sep}Downloads.")
                
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
            case "C":
                cfg = fl.CFG(os.path.join(settings.path, "iso-rename.cfg"))
                print("The current value is:", cfg.get_value())
                print("This option renames the ISO to something more recognisable.")
                iso_rename = ft.question("Rename an ISO after patching?")
                
                cfg.set_value(iso_rename)
                ft.clear_screen()
            case "D":
                cfg = fl.CFG(os.path.join(settings.path, "overwrite-perm.cfg"))
                print("The current value is:", cfg.get_value())
                print("This option allows the patcher to overwrite files.")
                overwrite_perm = ft.question("Allow files to be overwritten?")
                
                cfg.set_value(overwrite_perm)
                ft.clear_screen()
            case "E":
                cfg = fl.CFG(os.path.join(settings.path, "perf-monitor.cfg"))
                print("The current value is:", cfg.get_value())
                print("This option enables the performance monitor.")
                perf_monitor = ft.question("Enable the performance monitor?")
                
                cfg.set_value(perf_monitor)
                ft.clear_screen()
            case "F":
                cfg = fl.CFG(os.path.join(settings.path, "pref-language.cfg"))
                print("The current value is:", cfg.get_value())
                print("This option is the preferred language. If any language patch gets found during the installation process, it will pick this language.")
                
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
            case "G":
                cfg = fl.CFG(os.path.join(settings.path, "pycache.cfg"))
                print("The current value is:", cfg.get_value())
                print("The \"__pycache__\" folder gets generated by Python for caching purposes. This option deletes it after patching.")
                delete_pycache = ft.question("Delete the \"__pycache__\" folder after patching?")
    
                cfg.set_value(delete_pycache)
                ft.clear_screen()
            case "H":
                cfg = fl.CFG(os.path.join(settings.path, "riivo-suffix.cfg"))
                print("The current value is:", cfg.get_value())
                print("This option renames a Riivolution build so two or more can be installed at once.")
                riivo_suffix = ft.question("Add a suffix to Riivolution builds after patching?")
                
                cfg.set_value(riivo_suffix)
                ft.clear_screen()
            case "S":
                standard = ft.question("Enter default settings?")
                if standard:
                    standards = [cwd, cwd, True, True, True, "E", True, False]
                    for value, setting in zip(standards, cs.settings):
                        cfg = fl.CFG(os.path.join(settings.path, f"{setting}.cfg"))
                        cfg.set_value(value)
                ft.clear_screen()
            case "X":
                break
            case _:
                print("This is not an option. Please try again.")
    
    input("All done!")

if __name__ == "__main__":
    main()
