import Intermezzo_functions as im
import os
import subprocess as sp
import shutil as sh
import platform as pf

cwd = os.getcwd()

# Locates the ISO
while True:
    og_iso_name, og_iso = im.find_iso()
    if bool(og_iso_name):
        break
    else:
        print("No ISO/WBFS was found!")
        input("Please put an ISO/WBFS next to the script files. (Press enter to restart): ")

# Defines which type of Intermezzo needs to be installed
while True:
    choice = str(input("Which type of Intermezzo should be installed? (Regular or Texture): "))
    
    if choice in im.opt_list[0:4]:
        pre = "mkw-intermezzo"
        patch2_dl = "https://cdn.discordapp.com/attachments/870580346033430549/1112290380034080838/patch2.tar"
        break
    elif choice in im.opt_list[4:8]:
        pre = "tmp"
        patch2_dl = "https://cdn.discordapp.com/attachments/870580346033430549/1112290692870459432/patch2.tar"
        break
    else:
        print("This is not an option. Please try again.")
        
# Makes a list of Intermezzos available
print("Importing available Intermezzos...")
options = []
d = im.date()
k = 0

if pre == "mkw-intermezzo":
    for k in range(60):
        if im.check_date_existance(d - k, pre):
            options.append(str(d - k))
else:
    option_name = []
    option_index = []
    while True:
        if im.check_date_existance(d - k, "recent-080-hacks"):
            date = str(d - k)
            break
        k = k + 1
    
    for h in sorted(im.name_dict.items()):
        try:
            prefix = h[0][0] + "." + h[0][1] + "-" + h[1]
        except IndexError:
            prefix = h[1]
        if im.check_date_existance(date, prefix):
            options.append(h[1])
            option_name.append(im.clean_name[h[0]])
            option_index.append(h[0])

# Defines which Intermezzo needs to be installed
if pre == "mkw-intermezzo":
    for h in range(len(options)):
        print(chr(h + 65), ". ", options[h], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): "))
        index = ord(choice.upper()) - 65
        
        if index in range(len(options)):
            date = options[index]
            break
        else:
            print("This is not an option. Please try again.")
else:
    for h in range(len(options)):
        print(option_index[h], ". ", option_name[h], sep = "")

    while True:
        choice = str(input("Which Intermezzo should be installed? (Enter the corresponding option): "))
        
        for h in range(len(option_index)):
            if choice == option_index[h]:
                try:
                    pre = option_index[h][0] + "." + option_index[h][1] + "-" + options[h]
                except IndexError:
                    pre = options[h]
                break
        
        if pre == "tmp":
            print("This is not an option. Please try again.")
        else:
            break

# Directory setup before downloading
intermezzo = pre + "-" + date
directory = os.path.join(cwd, intermezzo)
txz = intermezzo + ".txz"
tar = intermezzo + ".tar"
if pf.uname()[0] == "Windows":
    bat = os.path.join(directory, "create-images.bat")
else:
    bat = os.path.join(directory, "create-images.sh")

# Checks for patch2.tar and handles them if present
patch2 = os.path.join(cwd, "patch2.tar")

options = []
for identifier in im.Language.identifiers:
    patch_lang = os.path.join(cwd, "patch{}.tar".format(identifier))
    if os.path.exists(patch_lang):
        options.append(identifier)

if len(options) == 0:
    present = False
elif len(options) == 1:
    present = im.question("A {} patch2.tar has been found. Should this one be used?".format(im.Language(options[0]).language))
    if present:
        patch_lang = os.path.join(cwd, "patch{}.tar".format(options[0]))
        os.rename(patch_lang, patch2)
    else:
        os.remove(os.path.join(cwd, "patch{}.tar".format(options[0])))
elif os.path.exists(patch2):
    present = im.question("A patch2.tar has been found. Should this one be used?")
    if not present:
        os.remove(patch2)
else:
    present = True
    print("Multiple patches have been found.")
    for option in options:
        language = im.Language(option)
        print(language.identifier, "-", language.language)
    while True:
        choice = str(input("Which patch2.tar should be used? (Enter the corresponding letter): ")).upper()
        
        if choice in options:
            patch_lang = os.path.join(cwd, "patch{}.tar".format(choice))
            os.rename(patch_lang, patch2)
            options.remove(choice)
            for option in options:
                patch_lang = os.path.join(cwd, "patch{}.tar".format(option))
                os.remove(patch_lang)
            break
        else:
            print("This is not an option. Please try again.")

if not present:
    print("Downloading patch2.tar...")
    im.download_data(patch2_dl, patch2)

# Performance monitor option
v = im.question("Enable the performance monitor?")

if v:
    print("Extracting patch2.tar...")
    sp.run(["7z", "x", "patch2.tar"])
    lecode = os.path.join(cwd, "patch-dir", "lecode")
    lpar = os.path.join(lecode, "lpar.txt")
    os.system("wlect lpar \"{}\" > \"{}\" -BH".format(os.path.join(lecode, "lecode-JAP.bin"), lpar))
    
    im.edit_setting(lpar, "LIMIT-MODE", "LE$EXPERIMENTAL")
    im.edit_setting(lpar, "PERF-MONITOR", "2")
    
    for r in im.region_set:
        region = os.path.join(lecode, "lecode-{}.bin".format(r))
        os.system("wlect patch \"{}\" --lpar \"{}\" -o".format(region, lpar))
    
    os.remove(lpar)
    os.remove(patch2)
    sp.run(["7z", "a", "patch2.tar", "patch-dir"])
    sh.rmtree("patch-dir")

# Retrieves the Intermezzo
print("Downloading Intermezzo...")
if pre == "mkw-intermezzo":
    link = "https://download.wiimm.de/intermezzo/"
else:
    link = "https://download.wiimm.de/intermezzo/texture-hacks/"

download = link + intermezzo + ".txz"
im.download_data(download, txz)

# Extracts txz and tar
print("Extracting files...")
sp.run(["7z", "x", txz])
sp.run(["7z", "x", tar])

# Moves patch2.tar and ISO
os.rename(patch2, os.path.join(directory, "patch2.tar"))
os.rename(og_iso, os.path.join(directory, og_iso_name))

# Starts the script
os.chdir(directory)
sp.run([bat])
os.chdir(cwd)

# Cleans the directories
print("Cleaning directory...")
if os.path.exists(os.path.join(directory, "riiv-sd-card")):
    os.rename(os.path.join(directory, "riiv-sd-card", "riivolution"), os.path.join(cwd, "riivolution"))
    os.rename(os.path.join(directory, "riiv-sd-card", "Wiimm-Intermezzo"), os.path.join(cwd, "Wiimm-Intermezzo"))
else:
    iso_d = os.path.join(directory, "new-image")
    i = os.listdir(iso_d)[0]
    
    if i.endswith(".iso"):
        iso_name = i
        os.rename(os.path.join(iso_d, iso_name), os.path.join(cwd, iso_name))
    else:
        wbfs_d = os.path.join(iso_d, i)
        wbfs_name = os.listdir(wbfs_d)[0]
        os.rename(os.path.join(wbfs_d, wbfs_name), os.path.join(cwd, wbfs_name))
    
if os.path.exists(os.path.join(cwd, "Wiimm-Intermezzo")):
    v = im.question("Rename the Intermezzo so two or more can be installed at once?")
else:
    v = False
    
if v:
    while True:
        suffix = str(input("Where should the folder be moved to? (Enter the preferred suffix): "))
        
        if suffix.replace("-", "").isalnum():
            break
        else:
            print("The suffix can only contain dashes and alphabetic and numeric characters. Please try again.")
    
    riiv = os.path.join(cwd, "riivolution")
    riiw = os.path.join(cwd, "Wiimm-Intermezzo")
    xml = os.path.join(riiv, "Wiimm-Intermezzo.xml")
    
    f = open(xml, "r")
    txt = f.readlines()
    f.close()
    
    for k in range(len(txt)):
        s = txt[k]
        s = s.replace("WiimmIntermezzo", "WiimmIntermezzo" + suffix)
        s = s.replace("Wiimm-Intermezzo", "Wiimm-Intermezzo-" + suffix)
        txt[k] = s
    
    f = open(xml, "w")
    f.writelines(txt)
    f.close()
    
    os.rename(riiw, riiw + "-" + suffix)
    os.rename(xml, os.path.join(riiv, "Wiimm-Intermezzo-{}.xml".format(suffix)))

# Moves back the original ISO and deletes the rest
os.rename(os.path.join(directory, og_iso_name), og_iso)
os.remove(txz)
os.remove(tar)
sh.rmtree(directory)
for file in os.listdir():
    if file.startswith("PaxHeaders"):
        sh.rmtree(file)

input("All done!")