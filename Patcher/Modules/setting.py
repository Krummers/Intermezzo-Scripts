import os

import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
settings = fl.Folder(os.path.join(cwd, "Settings"))

class Setting(object):
    
    def __str__(self):
        return f"{self.name: <30}" + str(self.get_value())
    
    def __repr__(self):
        return f"{self.internal} ({self.get_value()})"
    
    def get_value(self):
        return self.cfg.get_value()
    
    def set_default(self):
        self.cfg.set_value(self.default)
        ft.clear_screen()
    
    def create(self, setting):
        if setting == "directory":
            return Directory()
        elif setting == "downloads":
            return Downloads()
        elif setting == "gesso":
            return Gesso()
        elif setting == "iso-rename":
            return ISORename()
        elif setting == "kumo":
            return Kumo()
        elif setting == "overwrite-perm":
            return OverwritePermission()
        elif setting == "perf-monitor":
            return PerformanceMonitor()
        elif setting == "pref-language":
            return PreferredLanguage()
        elif setting == "pycache":
            return Pycache()
        elif setting == "riivo-suffix":
            return RiivolutionSuffix()
        else:
            raise ValueError("unknown setting")

class Directory(Setting):
    
    def __init__(self):
        self.name = "Output directory"
        self.internal = "directory"
        self.default = cwd
        self.documentation = "This directory is the location the new build gets moved to after the patcher has finished."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
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
        
        self.cfg.set_value(directory)
        ft.clear_screen()

class Downloads(Setting):
    
    def __init__(self):
        self.name = "patch2.tar downloads"
        self.internal = "downloads"
        self.default = cwd
        self.documentation = "This directory is the folder that gets checked for recently downloaded patch2.tar."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
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
        
        self.cfg.set_value(directory)
        ft.clear_screen()
    
class Gesso(Setting):
    
    def __init__(self):
        self.name = "Feather model"
        self.internal = "gesso"
        self.default = "feather"
        self.documentation = "This option adds a Feather model over the Blooper."
        
        self.options = ["feather", "krummy"]
        self.display_options = ["Feather", "Krummy Feather"]
        
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def __str__(self):
        value = self.cfg.get_value()
        if value is None:
            return f"{self.name: <30}None"
        string = self.display_options[self.options.index(value)]
        return f"{self.name: <30}{string}"
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        for x in range(len(self.options)):
            print(chr(x + 65), ". ", self.display_options[x], sep = "")
        
        while True:
            gesso = str(input("Which model should be used? (Enter the corresponding option): "))
            
            if len(gesso) != 1:
                print("This is not an option. Please try again.")
            elif gesso.isalpha() and ord(gesso.upper()) - 65 in range(len(self.options)):
                gesso = ord(gesso.upper()) - 65
                break
            else:
                print("This is not an option. Please try again.")
        
        self.cfg.set_value(self.options[gesso])
        ft.clear_screen()

class ISORename(Setting):
    
    def __init__(self):
        self.name = "ISO rename"
        self.internal = "iso-rename"
        self.default = True
        self.documentation = "This option renames the ISO to something more recognisable."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        rename = ft.question("Rename an ISO after patching?")
        self.cfg.set_value(rename)
        ft.clear_screen()

class Kumo(Setting):
    
    def __init__(self):
        self.name = "Thunder Cloud model"
        self.internal = "kumo"
        self.default = "normal"
        self.documentation = "This option adds a custom Thunder Cloud model over the Thunder Cloud."
        
        self.options = ["normal", "flipped-thunder", "mega", "pac-man", "sad-cat"]
        self.display_options = ["Normal", "Flipped Shock", "Mega Thunder Cloud", \
                                "PAC-Cloud", "Sad Cat Thunder Cloud"]
        
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def __str__(self):
        value = self.cfg.get_value()
        if value is None:
            return f"{self.name: <30}None"
        string = self.display_options[self.options.index(value)]
        return f"{self.name: <30}{string}"
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        
        for x in range(len(self.options)):
            print(chr(x + 65), ". ", self.display_options[x], sep = "")
        
        while True:
            kumo = str(input("Which model should be used? (Enter the corresponding option): "))
            
            if len(kumo) != 1:
                print("This is not an option. Please try again.")
            elif kumo.isalpha() and ord(kumo.upper()) - 65 in range(len(self.options)):
                kumo = ord(kumo.upper()) - 65
                break
            else:
                print("This is not an option. Please try again.")
        
        self.cfg.set_value(self.options[kumo])
        ft.clear_screen()

class OverwritePermission(Setting):
    
    def __init__(self):
        self.name = "File overwrite permission"
        self.internal = "overwrite-perm"
        self.default = True
        self.documentation = "This option allows the patcher to overwrite files."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        permission = ft.question("Allow files to be overwritten?")
        self.cfg.set_value(permission)
        ft.clear_screen()

class PerformanceMonitor(Setting):
    
    def __init__(self):
        self.name = "Performance monitor"
        self.internal = "perf-monitor"
        self.default = True
        self.documentation = "This option enables the performance monitor."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        monitor = ft.question("Enable the performance monitor?")
        self.cfg.set_value(monitor)
        ft.clear_screen()

class PreferredLanguage(Setting):
    
    def __init__(self):
        self.name = "Preferred language"
        self.internal = "pref-language"
        self.default = "E"
        self.documentation = "This option is the preferred language. If any language patch gets found during the installation process, it will pick this language automatically."
        
        self.options = ["B", "Q", "Z", "D", "G", "L", "E", "S", "H", \
                       "F", "I", "J", "K", "M", "N", "O", "P", "R", \
                       "W", "U"]
        self.display_options = ["Portuguese (NTSC)", "French (NTSC)", "Czech", "Danish", \
                                "German", "Greek", "English (PAL)", "Spanish (PAL)", \
                                "Finnish", "French (PAL)", "Italian", "Japanese", \
                                "Korean", "Spanish (NTSC)", "Dutch", "Polish", \
                                "Portuguese (PAL)", "Russian", "Swedish", "English (NTSC)"]
        
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def __str__(self):
        value = self.cfg.get_value()
        if value is None:
            return f"{self.name: <30}None"
        string = self.display_options[self.options.index(value)]
        return f"{self.name: <30}{string}"
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        
        for identifier in self.options:
            print(identifier, ". ", self.display_options[self.options.index(identifier)], sep = "")
        
        while True:
            language = str(input("What is your preferred language? (Enter the correct identifier): ")).upper()
            
            if language in self.options:
                break
            else:
                print("This is not an option. Please try again.")
        
        self.cfg.set_value(language)
        ft.clear_screen()

class Pycache(Setting):
    
    def __init__(self):
        self.name = "Pycache folder"
        self.internal = "pycache"
        self.default = True
        self.documentation = "The \"__pycache__\" folder gets generated by Python for caching purposes. This option deletes it after patching."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        delete = ft.question("Delete the \"__pycache__\" folder after patching?")
        self.cfg.set_value(delete)
        ft.clear_screen()

class RiivolutionSuffix(Setting):
    
    def __init__(self):
        self.name = "Riivolution suffix"
        self.internal = "riivo-suffix"
        self.default = False
        self.documentation = "This option renames a Riivolution build so two or more can be installed at once."
        self.cfg = fl.CFG(os.path.join(settings.path, f"{self.internal}.cfg"))
    
    def set_value(self):
        print(f"The current value is: {self.get_value()}")
        print(self.documentation)
        suffix = ft.question("Add a suffix to Riivolution builds after patching?")
        self.cfg.set_value(suffix)
        ft.clear_screen()
