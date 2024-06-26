import Intermezzo_settings as it
import os
import subprocess as sp
import shutil as sh
import platform as pf

import Modules.constants as cs
import Modules.date as dt
import Modules.file as fl
import Modules.functions as ft
import Modules.setting as st

cwd = os.getcwd()
cache = fl.Folder(os.path.join(cwd, "Cache"))
files = fl.Folder(os.path.join(cwd, "Files"))

# Check if all settings are defined
while True:
    if not all([st.Setting().create(setting).get_value() != None for setting in cs.settings]):
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

# Check if all user-defined directories exist
while True:
    if not all([os.path.exists(st.Setting().create(setting).get_value()) \
                for setting in ["directory", "downloads"]]):
        print("Not all drives are accessible!")
        input("Please make all drives defined in the settings available. (Press enter to restart): ")
    else:
        break

# Move downloaded patches into main directory
downloads = st.Setting().create("downloads").get_value()
for identifier in cs.identifiers + ["2"]:
    file = fl.File(os.path.join(downloads, f"patch{identifier}.tar"))
    if file.exists():
        file.move(os.path.join(cwd, file.filename))

# Define which type of Intermezzo needs to be installed
while True:
    choice = str(input("Which type of Intermezzo should be installed? (Regular or Texture): ")).lower()
    
    if choice in cs.types[:2]:
        prefix = "mkw-intermezzo"
        break
    elif choice in cs.types[2:]:
        prefix = ""
        break
    else:
        print("This is not an option. Please try again.")

# Make a list of Intermezzi available
print("Importing available Intermezzi...")
options = []
date = dt.Date()
x = 0

if prefix == "mkw-intermezzo":
    regular = fl.CHC(os.path.join(cache.path, "regular.chc"))
    if not regular.exists():
        date = dt.Date()
        regular_cache = []
        for x in range(60):
            if (date - x).intermezzo(prefix):
                options.append(str(date - x))
                regular_cache.append(date - x)
    else:
        regular_cache = regular.get_value()
        date = dt.Date()
        for x in range(len(regular_cache)):
            if not regular_cache[x].intermezzo(prefix):
                regular_cache = regular_cache[:x]
                break
        latest_known = regular_cache[0]
        for x in range(1, latest_known.difference(date) + 1):
            if (latest_known + x).intermezzo(prefix):
                regular_cache.insert(0, latest_known + x)
        options = [str(date) for date in regular_cache]
    regular.set_value(regular_cache)
else:
    texture = fl.CHC(os.path.join(cache.path, "texture.chc"))
    if not texture.exists():
        while True:
            if (date - x).intermezzo("texture-hacks"):
                date = date - x
                break
            x += 1
        
        texture_cache = {"date": date}
        choices = []
        options = []
        for item in cs.names.items():
            slot, name = item[0], item[1]
            if slot.isnumeric():
                codename = slot[0] + "." + slot[1] + "-" + cs.codenames[slot]
            else:
                codename = cs.codenames[slot]
            if date.intermezzo(codename):
                choices.append(slot)
                options.append(cs.names[slot])
        texture_cache["slots"] = choices
        date = str(date)
    else:
        texture_cache = texture.get_value()
        date = texture_cache["date"]
        if not date.intermezzo("texture-hacks"):
            date = dt.Date()
            while True:
                if (date - x).intermezzo("texture-hacks"):
                    date = date - x
                    break
                x += 1
        
        texture_cache["date"] = date
        slots = texture_cache["slots"]
        choices = []
        options = []
        for slot in slots:
            if slot.isnumeric():
                codename = slot[0] + "." + slot[1] + "-" + cs.codenames[slot]
            else:
                codename = cs.codenames[slot]
            if date.intermezzo(codename):
                for x in range(slots.index(slot), len(slots)):
                    choices.append(slots[x])
                    options.append(cs.names[slots[x]])
                break
        
        texture_cache["slots"] = slots
        date = str(date)
    texture.set_value(texture_cache)

# Define which Intermezzo needs to be installed
if prefix == "mkw-intermezzo":
    for x in range(len(options)):
        print(chr(x + 65), ". ", options[x], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): ")).upper()
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif choice.isalpha() and ord(choice.upper()) - 65 in range(len(options)):
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
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): ")).upper()
        
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
pref_language = st.Setting().create("pref-language").get_value()

options = []
for identifier in cs.identifiers:
    patchX = fl.TAR(os.path.join(cwd, f"patch{identifier}.tar"))
    if patchX.exists():
        options.append(identifier)

if patch2.exists():
    present = True
elif len(options) == 0:
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
else:
    for option in options:
        language = cs.languages[cs.identifiers.index(option)]
        print(option, ". ", language, sep = "")
    
    while True:
        if pref_language not in options:
            choice = str(input("Which patch2.tar should be used? (Enter the corresponding option): ")).upper()
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
    file = fl.TAR(os.path.join(files.path, "patch2", "200cc.tar" if prefix == "mkw-intermezzo" else "ri.tar"))
    file.copy(patch2.path)

# Setup directory before patching
intermezzo = prefix + "-" + date
directory = fl.Folder(os.path.join(cwd, intermezzo))
txz = fl.TXZ(os.path.join(cwd, intermezzo + ".txz"))
if pf.uname()[0] == "Windows":
    script = [["create-images-32.bat"]]
else:
    script = [["chmod", "+x", "create-images.sh"], ["./create-images.sh"]]

# Download Intermezzo
if prefix == "mkw-intermezzo":
    link = "https://download.wiimm.de/intermezzo/"
else:
    link = "https://download.wiimm.de/intermezzo/texture-hacks/"
link = link + intermezzo + ".txz"
ft.download(link, txz.path, progress = "Intermezzo")

# Extract TXZ and TAR
print("Extracting files...")
txz.extract()
tar = fl.TAR(txz.tar)
tar.extract()

# Execute gesso, kumo and perf-monitor setting
gesso = st.Setting().create("gesso").get_value()
kumo = st.Setting().create("kumo").get_value()
perf_monitor = st.Setting().create("perf-monitor").get_value()

if gesso != "feather" or kumo != "normal" or perf_monitor:
    patch2.extract()
    race = fl.File(os.path.join(patch2.extract_folder, "files", "Scene", "UI", "Race.szs"))
    
    if gesso != "feather":
        print(f"Copying {gesso}...")
        brres = fl.File(os.path.join(patch2.extract_folder, "common", "gesso.brres"))
        other = fl.File(os.path.join(files.path, "gesso", f"{gesso}.brres"))
        brres.delete()
        other.copy(brres.path)
        
        os.system(f"wszst extract \"{race.path}\"")
        tpl = fl.File(os.path.join(patch2.extract_folder, "files", "Scene", \
                      "UI", "Race.d", "game_image", "timg", "fm_item_gesso.tpl"))
        other = fl.File(os.path.join(files.path, "gesso", f"{gesso}.tpl"))
        tpl.delete()
        other.copy(tpl.path)
        os.system(f"wszst create \"{race.path[:-3] + 'd'}\" -o")
        sh.rmtree(race.path[:-3] + "d")
    
    if kumo != "normal":
        print(f"Copying {kumo}...")
        brres = fl.File(os.path.join(patch2.extract_folder, "common", "kumo.brres"))
        other = fl.File(os.path.join(files.path, "kumo", f"{kumo}.brres"))
        other.copy(brres.path)
        
        os.system(f"wszst extract \"{race.path}\"")
        tpl = fl.File(os.path.join(patch2.extract_folder, "files", "Scene", \
                      "UI", "Race.d", "game_image", "timg", "fm_item_pikakumo.tpl"))
        other = fl.File(os.path.join(files.path, "kumo", f"{kumo}.tpl"))
        tpl.delete()
        other.copy(tpl.path)
        os.system(f"wszst create \"{race.path[:-3] + 'd'}\" -o")
        sh.rmtree(race.path[:-3] + "d")
    
    if perf_monitor:
        print("Enabling the performance monitor...")
        lpar = fl.TXT(os.path.join(patch2.extract_folder, "lecode", "lpar.txt"))
        jap = fl.File(os.path.join(lpar.folder, "lecode-JAP.bin"))
        os.system(f"wlect lpar \"{jap.path}\" > \"{lpar.path}\" -BH")
        lpar.rewrite(lpar.find("LIMIT-MODE"), "LIMIT-MODE\t= LE$EXPERIMENTAL")
        lpar.rewrite(lpar.find("PERF-MONITOR"), "PERF-MONITOR\t= 2")
        
        for region in cs.regions:
            lebin = fl.File(os.path.join(lpar.folder, f"lecode-{region}.bin"))
            os.system(f"wlect patch \"{lebin.path}\" --lpar \"{lpar.path}\" -o")
        
        lpar.delete()
    
    patch2.build()

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
riivo_suffix = st.Setting().create("riivo-suffix").get_value()
if riivolution.exists() and riivo_suffix:
    print("Adding suffix to Riivolution build...")
    suffix = date if prefix == "mkw-intermezzo" else intermezzo
    riivolution, Wiimm_Intermezzo = ft.rename_riivolution(riivolution, Wiimm_Intermezzo, suffix)

# Execute iso-rename setting
iso_rename = st.Setting().create("iso-rename").get_value()
if new_iso.exists() and iso_rename:
    print("Renaming ISO...")
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
directory = fl.Folder(st.Setting().create("directory").get_value())
overwrite = st.Setting().create("overwrite-perm").get_value()

old_iso = os.path.join(directory.path, new_iso.filename)

print("Moving new build...")

if riivolution.exists() and Wiimm_Intermezzo.exists():
    if overwrite:
        fl.Folder(os.path.join(directory.path, riivolution.filename)).merge(riivolution)
        fl.Folder(os.path.join(directory.path, Wiimm_Intermezzo.filename)).merge(Wiimm_Intermezzo)
    else:
        x = 1
        check = os.path.join(directory.path, Wiimm_Intermezzo.filename)
        while os.path.exists(check):
            x += 1
            check = os.path.join(directory.path, f"{Wiimm_Intermezzo.filename}-{x}")
        if x > 1:
            suffix = Wiimm_Intermezzo.filename[len("Wiimm-Intermezzo-"):]
            riivolution, Wiimm_Intermezzo = ft.rename_riivolution(riivolution, Wiimm_Intermezzo, f"{suffix}-{x}")
        fl.Folder(os.path.join(directory.path, riivolution.filename)).merge(riivolution)
        Wiimm_Intermezzo.move(os.path.join(directory.path, Wiimm_Intermezzo.filename))
if new_iso.exists():
    if os.path.exists(old_iso) and overwrite:
        os.remove(old_iso)
    x = 1
    name = new_iso.filename
    check = os.path.join(directory.path, new_iso.filename)
    while os.path.exists(check):
        x += 1
        name = new_iso.filename[new_iso.filename.rfind("."):] + f"-{x}" + new_iso.filename[:new_iso.filename.rfind(".")]
        check = os.path.join(directory.path, name)
    if x > 1:
        new_iso.rename(name)
    new_iso.move(os.path.join(directory.path, new_iso.filename))

# Execute pycache setting
delete_pycache = st.Setting().create("pycache").get_value()
pycache = fl.Folder(os.path.join(cwd, "__pycache__"))

if pycache.exists() and delete_pycache:
    print("Deleting \"__pycache__\" folder...")
    pycache.delete()

input("All done!")
