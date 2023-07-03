import Generator_functions as gt
import os
import subprocess as sp
import shutil as sh

cwd = os.getcwd()

# Defines which type of Intermezzo needs to be installed
while True:
    choice = str(input("Which type of Intermezzo should be patched? (Regular or Texture): "))
    
    if choice in gt.opt_list[0:4]:
        pre = "mkw-intermezzo"
        break
    elif choice in gt.opt_list[4:8]:
        pre = "tmp"
        break
    else:
        print("This is not an option. Please try again.")

# Makes a list of Intermezzos available
print("Importing available Intermezzos...")
options = []
d = gt.date()
k = 0

if pre == "mkw-intermezzo":
    for k in range(60):
        if gt.check_date_existance(d - k, pre):
            options.append(str(d - k))
else:
    option_name = []
    option_index = []
    while True:
        if gt.check_date_existance(d - k, "recent-080-hacks"):
            date = str(d - k)
            break
        k = k + 1
    
    for h in sorted(gt.name_dict.items()):
        try:
            prefix = h[0][0] + "." + h[0][1] + "-" + h[1]
        except IndexError:
            prefix = h[1]
        if gt.check_date_existance(date, prefix):
            options.append(h[1])
            option_name.append(gt.clean_name[h[0]])
            option_index.append(h[0])

# Defines which Intermezzo needs to be edited
if pre == "mkw-intermezzo":
    for h in range(len(options)):
        print(chr(h + 65), ". ", options[h], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be patched? (Enter the corresponding option): "))
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
        choice = str(input("Which Intermezzo should be edited? (Enter the corresponding option): "))
        
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

# Defines to which language should be translated
for k in sorted(gt.lang_set):
    print(k, "-", gt.lang_dict[k])

while True:
    language = str(input("Which language should be translated to? (Enter the correct abbreviation): "))
    
    if language not in gt.lang_set:
        print("This is not an option. Please try again.")
    else:
        break

# Defines which patches should be applied
print("200 - 200cc\nRI - Random Items")
while True:
    patch_type = str(input("Which patches should be applied? (200 or RI): "))
    
    if patch_type == "200":
        break
    elif patch_type.lower() == "ri":
        patch_type = "ri"
        break
    else:
        print("This is not an option. Please try again.")

# Directory setup before downloading
print("Setting up directory...")
intermezzo = pre + "-" + date
directory = os.path.join(cwd, intermezzo)
txz = intermezzo + ".txz"
tar = intermezzo + ".tar"

# Retrieves the Intermezzo
print("Downloading Intermezzo...")
if pre == "mkw-intermezzo":
    link = "https://download.wiimm.de/intermezzo/"
else:
    link = "https://download.wiimm.de/intermezzo/texture-hacks/"

download = link + intermezzo + ".txz"

gt.download_data(download, txz)

# Extracts txz and tar
print("Extracting Intermezzo...")
sp.run("7z x {}".format(txz))
sp.run("7z x {}".format(tar))

# Retrieves track list information from patch.tar and translates it
print("Translating track listing...")
patch = os.path.join(cwd, "patch.tar")
os.rename(os.path.join(directory, "patch.tar"), patch)

sp.run("7z x patch.tar")
os.rename(os.path.join(cwd, "patch-dir", "bmg", "track-names", "_base.txt"), os.path.join(cwd, "translate.txt"))

info = gt.read_file("translate.txt")
prefixes = gt.get_prefix_list()

translated = 0
total = 0
wiiki = gt.Wiiki()

for k in range(len(info)):
    # Checks if a line is a track
    if len(info[k]) < 7:
        continue
    l = info[k].split("\\n")
    if l[1] == "-":
        continue
    
    # Extracts needed information from the line
    if (pos := l[1].find("(")) != -1:
        track = l[1][:pos - 1]
        parenthesis = l[1][pos + 1:-1]
    else:
        track = l[1]
        parenthesis = ""
    track_type = l[6]
    prefix = l[7]
    colour_prefixes = l[9]
    colour_version = l[10]
    
    # Translates the track name
    translation = wiiki.translate(prefix + track, language)
    
    # Translation ratio
    total += 1
    if translation != None:
        translated += 1
    
    if translation == None and parenthesis != "":
        translation = prefix + track + " (" + parenthesis + ")"
        colour_version = colour_version + " \\z{800,46}\\c{yor7}(NT)"
    elif translation == None and parenthesis == "":
        translation = prefix + track
        colour_version = colour_version + " \\z{800,46}\\c{yor7}(NT)"
    
    # Removes prefix from translation
    for p in prefixes:
        if translation.startswith(p + " "):
            prefix = p
            translation = translation[len(p) + 1:]
            break
        prefix = ""
    
    # Inserting new information
    l[0] = l[0][0:l[0].find("=") + 5] + translation.lower() + " " + parenthesis + l[0][-3:]
    slot = l[0][2:l[0].find("\t")]
    if slot in gt.slot_dict.keys():
        l[0] = l[0].replace(slot, gt.slot_dict[slot])
    
    if parenthesis != "":
        l[1] = translation + " (" + parenthesis + ")"
        l[13] = track_type + translation + " (" + parenthesis + ")\n"
    else:
        l[1] = translation
        l[13] = track_type + translation + "\n"
    
    if prefix != "":
        l[7] = prefix + " "
    
    for p, q in zip(["SFC", "64", "GC", "Wii U"], ["SNES", "N64", "GCN", "WiiU"]):
        if prefix == p:
            l[9] = colour_prefixes[:colour_prefixes.find(q)] + prefix + colour_prefixes[-8:]
    
    l[10] = colour_version
    
    info[k] = l
    # Printing results
    if prefix != "":
        print("Translation to {} is {} {}.".format(gt.lang_dict[language], prefix, translation))
    else:
        print("Translation to {} is {}.".format(gt.lang_dict[language], translation))

print("Translated {} of {} names.".format(translated, total))
print("Translation ratio is {}%.".format(round((translated / total) * 100, 2)))

for k in range(len(info)):
    if type(info[k]) == str:
        continue
    info[k] = "\\n".join(info[k])

gt.write_file("translate.txt", info)

# Makes a setup for patch2.tar
print("Preparing patch2.tar...")
clean_files = os.path.join(cwd, "clean-files")
patch_dir = os.path.join(cwd, "patch-dir")

sh.rmtree(patch_dir)
sh.copytree(clean_files, patch_dir)

gt.extract_folder_option(patch_dir, patch_type)
gt.extract_folder_option(os.path.join(patch_dir, "lecode"), patch_type)

# Edits text files for patch2.tar
print("Writing text files...")
for k in {"_base.txt", "en-all.txt", "en-nin.txt"}:
    sh.copyfile("translate.txt", os.path.join(patch_dir, "bmg", "track-names", k))

os.rename(os.path.join(patch_dir, "bmg", "messages", "force.txt"), "force.txt")

rename = [(6, "  M01	= \c{blue1}Intermezzo " + date), \
          (15, "   7e2	= \c{blue1}Intermezzo " + date), \
          (16, "   838	= \c{blue1}Intermezzo " + date), \
          (18, "  1004	= \c{blue1}Intermezzo " + date), \
          (19, "  106f	= \c{blue1}VS, Intermezzo " + date), \
          (20, "  1070	= \c{blue1}Battle, Intermezzo " + date), \
          (21, "  10d7	= Private region for Intermezzo " + date + ".")]

for k, l in rename:
    gt.rewrite_line("force.txt", k, l + "\n")

for k in {"force.txt", "force-G.txt", "force-S.txt"}:
    sh.copyfile("force.txt", os.path.join(patch_dir, "bmg", "messages", k))
    
# Makes patch2.tar
print("Creating patch2.tar...")
sp.run("7z a patch2.tar \"{}\"".format(patch_dir))

# Cleaning directory
print("Cleaning directory...")
os.remove("translate.txt")
os.remove("force.txt")
os.remove(txz)
os.remove(tar)
os.remove(patch)
sh.rmtree(intermezzo)
sh.rmtree(patch_dir)

input("All done!")