import Intermezzo_settings as it
import os
import subprocess as sp
import shutil as sh
import platform as pf

import Modules.constants as cs
import Modules.date as dt
import Modules.file as fl
import Modules.functions as ft

cwd = os.getcwd()
settings = fl.Folder(os.path.join(cwd, "Settings"))

# Check if all settings are defined
while True:
    if not all([fl.CFG(os.path.join(settings.path, setting + ".cfg")).exists() for setting in cs.settings]):
        print("Not all settings are defined!")
        it.main()
    else:
        break

# Locate ISO
while True:
    for file in os.listdir(cwd):
        for extension in cs.extensions:
            if file.endswith(extension):
                iso = fl.File(os.path.join(cwd, file))
                break_loop = True
                break
            break_loop = False
        if break_loop:
            break
        break_loop = False
    if break_loop:
        break
    print("No ISO was found!")
    input("Please put an ISO in this directory. (Press enter to restart): ")

# Define which type of Intermezzo needs to be installed
while True:
    choice = str(input("Which type of Intermezzo should be installed? (Regular or Texture): ")).lower()
    
    if choice in cs.types[:2]:
        prefix = "mkw-intermezzo"
        patch2_download = "https://cdn.discordapp.com/attachments/870580346033430549/1112290380034080838/patch2.tar"
        break
    elif choice in cs.types[2:]:
        prefix = ""
        patch2_download = "https://cdn.discordapp.com/attachments/870580346033430549/1112290692870459432/patch2.tar"
        break
    else:
        print("This is not an option. Please try again.")

# Make a list of Intermezzos available
print("Importing available Intermezzos...")
options = []
date = dt.Date()
x = 0

if prefix == "mkw-intermezzo":
    date = dt.Date()
    for x in range(60):
        if (date - x).intermezzo(prefix):
            options.append(str(date - x))
else:
    choices = []
    options = []
    while True:
        if (date - x).intermezzo("recent-080-hacks"):
            date = date - x
            break
        x += 1
    
    for item in cs.names.items():
        slot, name = item[0], item[1]
        if slot.isnumeric():
            codename = slot[0] + "." + slot[1] + "-" + cs.codenames[slot]
        else:
            codename = cs.codenames[slot]
        if date.intermezzo(codename):
            choices.append(slot)
            options.append(cs.names[slot])
    date = str(date)

# Define which Intermezzo needs to be installed
if prefix == "mkw-intermezzo":
    for x in range(len(options)):
        print(chr(x + 65), ". ", options[x], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): "))
        
        if all([choice.isalpha(), len(choice) == 1, ord(choice.upper()) - 65 in range(len(options))]):
            choice = ord(choice.upper()) - 65
            date = options[choice]
            title = "Intermezzo"
            break
        else:
            print("This is not an option. Please try again.")
else:
    for x in range(len(options)):
        print(choices[x], ". ", options[x], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): "))
        
        if choice in choices:
            index = choices.index(choice)
            if choice.isnumeric():
                prefix = choice[0] + "." + choice[1] + "-" + cs.codenames[choice]
            else:
                prefix = cs.codenames[choice]
                title = cs.names[choice]
            break
        else:
            print("This is not an option. Please try again.")

# Check and handle patch2.tar
patch2 = fl.TAR(os.path.join(cwd, "patch2.tar"))
pref_language = fl.CFG(os.path.join(settings.path, "pref-language.cfg")).get_value()

options = []
for identifier in cs.identifiers:
    patchX = fl.TAR(os.path.join(cwd, f"patch{identifier}.tar"))
    if patchX.exists():
        options.append(identifier)

if len(options) == 0:
    present = False
elif len(options) == 1:
    identifier = options[0]
    if pref_language != identifier:
        print(f"A {cs.languages[cs.identifiers.index(identifier)]} patch2.tar has been found.")
        choice = ft.question("Use this patch2.tar?")
    else:
        choice = True
        
    patchX = fl.TAR(os.path.join(cwd, f"patch{identifier}.tar"))
    if choice:
        present = True
        patchX.rename(patch2.path)
    else:
        patchX.delete()
        present = False
elif patch2.exists():
    present = True
else:
    for option in options:
        language = cs.languages[cs.identifiers.index(option)]
        print(option, ". ", language, sep = "")
    
    while True:
        if pref_language not in options:
            choice = str(input("Which patch2.tar should be used? (Enter the corresponding option): "))
        else:
            choice = pref_language
        
        if choice in options:
            options.remove(choice)
            for option in options:
                patchX = fl.TAR(os.path.join(cwd, f"patch{option}.tar"))
                patchX.delete()
            patchX = fl.TAR(os.path.join(cwd, f"patch{choice}.tar"))
            patchX.rename(patch2.path)
            present = True
            break
        else:
            print("This is not an option. Please try again.")

if not present:
    print("Downloading patch2.tar...")
    ft.download(patch2_download, patch2.path)

# Execute perf-monitor setting
perf_monitor = fl.CFG(os.path.join(settings.path, "perf-monitor.cfg")).get_value()

if perf_monitor:
    print("Enabling the performance monitor...")
    patch2.extract()
    lpar = fl.TXT(os.path.join(patch2.extract_folder, "lecode", "lpar.txt"))
    jap = fl.File(os.path.join(lpar.folder, "lecode-JAP.bin"))
    os.system(f"wlect lpar \"{jap.path}\" > \"{lpar.path}\" -BH")
    lpar.rewrite(8, "LIMIT-MODE\t= LE$EXPERIMENTAL")
    lpar.rewrite(13, "PERF-MONITOR\t= 2")
    
    for region in cs.regions:
        lecode_bin = fl.File(os.path.join(lpar.folder, f"lecode-{region}.bin"))
        os.system(f"wlect patch \"{lecode_bin.path}\" --lpar \"{lpar.path}\" -o")
    
    lpar.delete()
    patch2.build()

# Setup directory before patching
intermezzo = prefix + "-" + date
directory = fl.Folder(os.path.join(cwd, intermezzo))
txz = fl.TXZ(os.path.join(cwd, intermezzo + ".txz"))
if pf.uname()[0] == "Windows":
    script = [["create-images.bat"]]
else:
    script = [["chmod", "+x", "create-images.sh"], ["./create-images.sh"]]

# Download Intermezzo
print("Downloading Intermezzo...")
if prefix == "mkw-intermezzo":
    link = "https://download.wiimm.de/intermezzo/"
else:
    link = "https://download.wiimm.de/intermezzo/texture-hacks/"
link = link + intermezzo + ".txz"
ft.download(link, txz.path)

# Extract TXZ and TAR
print("Extracting files...")
txz.extract()
tar = fl.TAR(txz.tar)
tar.extract()

# Move ISO and patch2.tar
patch2.move_down([intermezzo])
iso.move_down([intermezzo])

# Start script
os.chdir(directory.path)
for command in script:
    sp.run(command)
os.chdir(cwd)

# Clean directory
riivolution = fl.Folder(os.path.join(directory.path, "riiv-sd-card", "riivolution"))
Wiimm_Intermezzo = fl.Folder(os.path.join(directory.path, "riiv-sd-card", "Wiimm-Intermezzo"))
new_image = fl.Folder(os.path.join(directory.path, "new-image"))
if new_image.exists():
    subfolder = fl.Folder(os.path.join(new_image.path, os.listdir(new_image.path)[0]))
    new_iso = fl.File(os.path.join(subfolder.path, os.listdir(subfolder.path)[0]))
else:
    new_iso = fl.File(os.path.join(new_image.path, "nonexistent.iso"))

if riivolution.exists() and Wiimm_Intermezzo.exists():
    riivolution.move_up(2)
    Wiimm_Intermezzo.move_up(2)

if new_iso.exists():
    new_iso.move_up(3)

iso.move_up(1)
tar.delete()
txz.delete()
for file in os.listdir():
    if file.startswith("PaxHeaders"):
        sh.rmtree(file)

# Execute riivo-suffix setting
riivo_suffix = fl.CFG(os.path.join(settings.path, "riivo-suffix.cfg"))
if riivolution.exists() and riivo_suffix:
    suffix = date if prefix == "mkw-intermezzo" else intermezzo
    xml = fl.TXT(os.path.join(riivolution.path, "Wiimm-Intermezzo.xml"))
    lines = xml.read()
    for x in range(len(lines)):
        lines[x] = lines[x].replace("WiimmIntermezzo", f"WiimmIntermezzo{suffix}")
        lines[x] = lines[x].replace("Wiimm-Intermezzo", f"Wiimm-Intermezzo-{suffix}")
    xml.write(lines)
    xml.rename(f"Wiimm-Intermezzo-{suffix}.xml")
    Wiimm_Intermezzo.rename(f"Wiimm-Intermezzo-{suffix}")

# Execute iso-rename setting
iso_rename = fl.CFG(os.path.join(settings.path, "iso-rename.cfg"))
if new_iso.exists and iso_rename:
    for file in os.listdir():
        for extension in cs.extensions:
            if file.endswith(extension) and file != iso.filename:
                new_iso.rename(title + " " + date + "." + extension)
                break_loop = True
                break
            break_loop = False
        if break_loop:
            break
        break_loop = False

# Execute directory setting
directory = fl.Folder(fl.CFG(os.path.join(settings.path, "directory.cfg")).get_value())

if riivolution.exists() and Wiimm_Intermezzo.exists():
    riivolution.move(os.path.join(directory.path, riivolution.filename))
    Wiimm_Intermezzo.move(os.path.join(directory.path, Wiimm_Intermezzo.filename))
if new_iso.exists():
    new_iso.move(os.path.join(directory.path, new_iso.filename))

# Executes pycache setting
delete_pycache = fl.CFG(os.path.join(settings.path, "pycache.cfg"))
pycache = fl.Folder(os.path.join(cwd, "__pycache__"))

if pycache.exists() and delete_pycache:
    pycache.delete()

input("All done!")
