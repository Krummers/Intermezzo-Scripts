import Intermezzo_functions as im
import os
import subprocess as sp
import shutil as sh
import pyunpack as pu

cwd = os.getcwd()
config = os.path.join(cwd, "config.def")

# Defines which type of Intermezzo needs to be installed
while True:
    choice = str(input("Which type of Intermezzo should be installed? (Regular or Texture): "))
    
    if choice in im.opt_list[0:4]:
        pre = "mkw-intermezzo"
        patch2_dl = "https://cdn.discordapp.com/attachments/870580346033430549/1029086086544232489/patch2.tar"
        break
    elif choice in im.opt_list[4:8]:
        pre = "tmp"
        patch2_dl = "https://cdn.discordapp.com/attachments/870580346033430549/1029088364848234576/patch2.tar"
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
        print(option_index[h], ". ", options[h], sep = "")

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

# Defines script options in config.def if asked
if os.path.exists(config):
    while True:
        config_option = str(input("Should a new settings file be created? (Y or N): ")).lower()
        
        if config_option in im.yn:
            if config_option in im.yn[0:2]:
                os.remove(config)
            break
        else:
            print("This is not an option. Please try again.")
else:
    config_option = "yes"

if config_option in im.yn[0:2]:    
    # Defines game language
    for k in im.script_list[0:10]:
        print(k, "-", im.script_dict[k])
    
    while True:
        language = str(input("Which language should be used? (Enter the corresponding letter): ")).upper()
        
        if language == im.script_list[7]:
            print("Wiimm does not like Italian. Please pick another language.")
        elif language in im.script_list[0:10]:
            break
        else:
            print("This is not an option. Please try again.")
    
    # Defines fallback language
    if language in im.script_list[5:10]:
        for k in im.script_list[0:5]:
            print(k, "-", im.script_dict[k])
        
        while True:
            language2 = str(input("Which fallback language should be used? (Enter the corresponding letter): ")).upper()
            
            if language2 in im.script_list[0:5]:
                break
            else:
                print("This is not an option. Please try again.")
    else:
        language2 = language
    
    # Defines build type
    for k in range(1, 4):
        print(str(k) + ". " + im.script_dict[im.script_list[k + 9]])
    
    while True:
        build_type = int(input("Which type of Intermezzo needs to be built? (Enter the corresponding number): "))
        
        if build_type in range(1, 4):
            build_type = im.script_list[build_type + 9]
            break
        else:
            print("This is not an option. Please try again.")
    
    # Defines savegame
    if build_type in im.script_list[10:12]:
        while True:
            savegame = str(input("Does a seperate savegame need to be added? (Y or N): ")).lower()
            
            if savegame in im.yn[0:2]:
                savegame = "1"
                break
            elif savegame in im.yn[2:4]:
                savegame = "0"
                break
            else:
                print("This is not an option. Please try again.")
    else:
        split_iso = "1"
        savegame = "1"
    
    # Creates config.def
    f = open("config.def", "w")
    f.write("MSGLANG1=\"{}\"\n".format(language))
    f.write("MSGLANG2=\"{}\"\n".format(language2))
    f.write("ISOMODE=\"{}\"\n".format(build_type))
    if build_type == "riiv":
        f.write("SPLITISO=\"{}\"\n".format(split_iso))
    f.write("PRIV_SAVEGAME=\"{}\"\n".format(savegame))
    f.close()

# Directory setup before downloading
intermezzo = pre + "-" + date
directory = os.path.join(cwd, intermezzo)
txz = intermezzo + ".txz"
tar = intermezzo + ".tar"

print("Downloading and extracting files...")

# Retrieves the Intermezzo
if pre == "mkw-intermezzo":
    link = "https://download.wiimm.de/intermezzo/"
else:
    link = "https://download.wiimm.de/intermezzo/texture-hacks/"

download = link + intermezzo + ".txz"

im.download_data(download, txz)

# Retrieves the patch2.tar
patch2 = os.path.join(cwd, "patch2.tar")

im.download_data(patch2_dl, patch2)

# Locates the ISO
for f in os.listdir(cwd):
    if f.endswith(".iso") or f.endswith(".wbfs"):
        og_iso = os.path.join(cwd, f)
        og_iso_name = f
        break

# Extracts txz and tar
os.rename(txz, txz[0:-3] + "xz")
pu.Archive(txz[0:-3] + "xz").extractall(cwd)
os.rename(directory, tar)

pu.Archive(tar).extractall(cwd)
os.rename(txz[0:-3] + "xz", txz)

os.rename(patch2, txz[0:-4] + "\\patch2.tar")
os.rename(og_iso, txz[0:-4] + "\\" + og_iso_name)

# Moves config.def
os.rename(os.path.join(cwd, "config.def"), os.path.join(directory, "config.def"))

# Starts the script
os.chdir(directory)
sp.run(".\create-images.bat --autorun", stdin = sp.PIPE)
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

# Moves back the original ISO, config.def, and deletes the rest
os.rename(os.path.join(directory, og_iso_name), og_iso)
os.rename(os.path.join(cwd, directory, "config.def"), os.path.join(cwd, "config.def"))
os.remove(txz)
os.remove(tar)
sh.rmtree(directory)

print("All done!")
input("Press enter to close: ")