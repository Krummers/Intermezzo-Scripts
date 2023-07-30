import Intermezzo_functions as im
import os

cwd = os.getcwd()

while True:

    edit = im.question("Do you want to edit the settings?")
    
    if edit:
        files = os.listdir("Settings")
        for file, x in zip(files, range(len(files))):
            print(chr(x + 65), ". ", file[:-4], sep = "")
        
        while True:
            setting = str(input("Which setting should be edited? (Enter the corresponding letter): "))
            
            setting = ord(setting.upper()) - 65
            if setting <= len(files):
                setting = os.path.join(cwd, "Settings", files[setting])
                break
            else:
                print("This is not an option. Please try again.")
        
        print("The current value of this setting is:")
        information = im.read_file(setting)
        variant = information[0]
        value = information[1:]
        
        if variant == "bool":
            print(bool(int(value[0])))
            
            delete_pycache = im.question("Delete the __pycache__ folder after patching?")
            
            if delete_pycache:
                information = [variant + "\n", "1\n"]
                print("Setting set to: True")
            else:
                information = [variant + "\n", "0\n"]
                print("Setting set to: False")
            
            im.write_file(setting, information)
        elif variant == "directory":
            pass
    else:
        break

input("All done!")
