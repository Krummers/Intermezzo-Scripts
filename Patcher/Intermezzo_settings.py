import Intermezzo_functions as im
import os

while True:
    # Print all settings
    print("Current settings: ")
    [print(im.Setting(setting)) for setting in im.settings]
    
    # Print setting selection screen
    print()
    for setting, x in zip(im.settings, range(len(im.settings))):
        print(chr(x + 65), ". ", setting, sep = "")
    print("X. Exit the menu")
    
    setting = str(input("Which setting should be edited? (Enter the corresponding letter): ")).upper()
    
    match setting:
        case "A":
            print("The current value is:", im.Setting("directory").get_value())
            print("Enter the directory where the files should be moved to after patching, separated by a comma.")
            folders = str(input("Directory: ")).split(",")
            
            drive = os.path.splitdrive(os.getcwd())[0]
            
            directory = drive + os.sep
            for folder in folders:
                directory = os.path.join(directory, folder)
            
            im.Setting("directory").set_value(directory)
        case "B":
            print("The current value is:", im.Setting("iso-rename").get_value())
            iso_rename = im.question("Rename an ISO after patching?")
            
            im.Setting("iso-rename").set_value(iso_rename)
        case "C":
            print("The current value is:", im.Setting("pycache").get_value())
            delete_pycache = im.question("Delete the \"__pycache__\" folder after patching?")

            im.Setting("pycache").set_value(delete_pycache)
        case "D":
            print("The current value is:", im.Setting("riivo-suffix").get_value())
            riivo_suffix = im.question("Add a suffix to Riivolution builds after patching?")
            
            im.Setting("riivo-suffix").set_value(riivo_suffix)
        case "X":
            break
        case other:
            print("This is not an option. Please try again.")

input("All done!")
