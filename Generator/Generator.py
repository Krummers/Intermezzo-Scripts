import os
import subprocess as sp

import Modules.constants as cs
import Modules.date as dt
import Modules.file as fl
import Modules.functions as ft

import Modules.temporary_functions as tf

cwd = os.getcwd()
cache = fl.Folder(os.path.join(cwd, "Cache"))

# Define which type of Intermezzo needs to be edited
while True:
    choice = str(input("Which type of Intermezzo should be edited? (Regular or Texture): ")).lower()
    
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

# Define which Intermezzo needs to be edited
if prefix == "mkw-intermezzo":
    for x in range(len(options)):
        print(chr(x + 65), ". ", options[x], sep = "")
    
    while True:
        choice = str(input("Which Intermezzo should be edited? (Enter the corresponding option): "))
        
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
        choice = str(input("Which Intermezzo should be edited? (Enter the corresponding option): "))
        
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

# Define to which language should be translated
for identifier in cs.identifiers:
    print(identifier, ". ", cs.languages[cs.identifiers.index(identifier)], sep = "")

while True:
    language = str(input("Which language should be translated to? (Enter the corresponding option): "))
    
    if language.upper() in cs.identifiers:
        language = language.upper()
        break
    else:
        print("This is not an option. Please try again.")

# Define which mode should be applied
for x in range(len(cs.modes)):
    print(chr(x + 65), ". ", cs.modes[x], sep = "")

while True:
    mode = str(input("Which mode should be applied? (Enter the corresponding option): "))
    
    if len(mode) != 1:
        print("This is not an option. Please try again.")
    elif mode.isalpha() and ord(mode.upper()) - 65 in range(len(cs.modes)):
        mode = cs.modes[ord(mode.upper()) - 65]
        break
    else:
        print("This is not an option. Please try again.")

# Setup directory before patching
intermezzo = prefix + "-" + date
directory = fl.Folder(os.path.join(cwd, intermezzo))
txz = fl.TXZ(os.path.join(cwd, intermezzo + ".txz"))

# Download Intermezzo
print("Downloading Intermezzo...")
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

# Retrieves track list information from patch.tar and translates it
print("Translating track listing...")
patch = fl.TAR(os.path.join(directory.path, "patch.tar"))
patch.move_up(1)
patch.extract()

# Temporary code that needs to be rewritten
translations = fl.TXT(os.path.join(cwd, "patch-dir", "bmg", "track-names", "_base.txt"))
translations.move_up(3)
translations.rename("translate.txt")

info = tf.read_file(translations.path)
prefixes = tf.get_prefix_list()

translated = 0
total = 1
if language != "E":
    total = 0
    wiiki = tf.Wiiki()
    
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
        translation = wiiki.translate(prefix + track, cs.abbreviations[cs.identifiers.index(language)])
        
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
        if slot in tf.slot_dict.keys():
            l[0] = l[0].replace(slot, tf.slot_dict[slot])
        
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
            print("Translation to {} is {} {}.".format(cs.languages[cs.identifiers.index(language)], prefix, translation))
        else:
            print("Translation to {} is {}.".format(cs.languages[cs.identifiers.index(language)], translation))

# Already rewritten
print(f"Translated {translated} out of {total} names.")
print(f"Translation ratio is {translated / total * 100:.2f}%.")

statistics = fl.TXT(os.path.join(cwd, "Statistics.txt"))
results = f"* {cs.languages[cs.identifiers.index(language)]} - {translated}/{total} ({translated / total * 100:.2f}%)"

if not statistics.exists():
    statistics.write([f"{results}\n"])
else:
    statistics.append(results)

# End of already rewritten

for k in range(len(info)):
    if type(info[k]) == str:
        continue
    info[k] = "\\n".join(info[k])

tf.write_file("translate.txt", info)

# End of temporary code that needs to be rewritten

# Setup files for patch2.tar
print("Preparing patch2.tar...")
clean = fl.Folder(os.path.join(cwd, "Clean"))
patch_dir = fl.Folder(patch.extract_folder)

patch_dir.delete()
clean.copy(patch_dir.path)

for folder in os.listdir(patch_dir.path):
    folder = fl.Folder(os.path.join(patch_dir.path, folder))
    if folder.filename.endswith("-option") and not folder.filename.startswith(mode):
        folder.delete()

folder = fl.Folder(os.path.join(patch_dir.path, f"{mode}-option"))
for file in os.listdir(folder.path):
    file = fl.File(os.path.join(folder.path, file))
    file.move_up(1)
folder.delete()

# Edit text files for patch2.tar
for file in {"_base.txt", "en-all.txt", "en-nin.txt"}:
    translations.copy(os.path.join(patch_dir.path, "bmg", "track-names", file))

force = fl.TXT(os.path.join(patch_dir.path, "bmg", "messages", "force.txt"))
force.move_up(3)

force.rewrite(force.find("M01"), f"  M01\t= \\c{{blue1}}{title} {date}")
force.rewrite(force.find("7e2"), f"   7e3\t= \\c{{blue1}}{title} {date}")
force.rewrite(force.find("838"), f"   838\t= \\c{{blue1}}{title} {date}")
force.rewrite(force.find("1004"), f"  1004\t= \\c{{blue1}}{title} {date}")
force.rewrite(force.find("106f"), f"  106f\t= \\c{{blue1}}VS, {title} {date}")
force.rewrite(force.find("1070"), f"  1070\t= \\c{{blue1}}Battle, {title} {date}")
force.rewrite(force.find("10d7"), f"  10d7\t= Private region for {title} {date}")

for file in {"force.txt", "force-G.txt", "force-S.txt"}:
    force.copy(os.path.join(patch_dir.path, "bmg", "messages", file))
    
# Create patch2.tar
print("Creating patch2.tar...")
sp.run(f"7z a patch{language}.tar \"{patch_dir.path}\"")

# Clean directory
print("Cleaning directory...")
translations.delete()
force.delete()
tar.delete()
txz.delete()
patch.delete()

input("All done!")