import os
import subprocess as sp

import Modules.constants as cs
import Modules.date as dt
import Modules.file as fl
import Modules.functions as ft

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
        choice = str(input("Which Intermezzo should be edited? (Enter the corresponding option): ")).upper()
        
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
        choice = str(input("Which Intermezzo should be edited? (Enter the corresponding option): ")).upper()
        
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
    language = str(input("Which language should be translated to? (Enter the corresponding option): ")).upper()
    
    if language in cs.identifiers:
        break
    else:
        print("This is not an option. Please try again.")

# Define which mode should be applied
for x in range(len(cs.modes)):
    print(chr(x + 65), ". ", cs.modes[x], sep = "")

while True:
    mode = str(input("Which mode should be applied? (Enter the corresponding option): ")).upper()
    
    if len(mode) != 1:
        print("This is not an option. Please try again.")
    elif mode.isalpha() and ord(mode) - 65 in range(len(cs.modes)):
        mode = cs.modes[ord(mode) - 65]
        break
    else:
        print("This is not an option. Please try again.")

# Setup directory before patching
intermezzo = prefix + "-" + date
directory = fl.Folder(os.path.join(cwd, intermezzo))
txz = fl.TXZ(os.path.join(cwd, intermezzo + ".txz"))

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

# Retrieves track list information from patch.tar and translates it
print("Translating track listing...")
patch = fl.TAR(os.path.join(directory.path, "patch.tar"))
patch.move_up(1)
patch.extract()

# Download translation JSON and prepare translation process
json = ft.get_translations()
prefix_set = ft.get_prefixes()

translate = fl.TXT(os.path.join(cwd, "patch-dir", "bmg", "track-names", "_base.txt"))
translate.move_up(3)
translate.rename("translate.txt")

entries = translate.read()
translated = -30
total = 1

if language != "E":
    total = -32
    
    for k in range(len(entries)):
        # Check if an entry is a track
        if len(entries[k]) < 7:
            continue
        entry = entries[k].split("\\n")
        if entry[1] == "-":
            continue
        
        # Extract information
        message = entry[0]
        slot = message[2:message.find("\t")]
        track = entry[1]
        if "(" in track:
            extra_begin = entry[1].rfind("(")
            extra = track[extra_begin + 1:-1]
            track = track.replace(f" ({extra})", "")
        else:
            extra = ""
        track_type = entry[6]
        colour_prefixes = entry[9]
        prefixes = colour_prefixes.split("\\c{")
        prefixes = [prefix[prefix.find("}") + 1:].strip() for prefix in prefixes]
        prefixes = [prefix for prefix in prefixes if prefix in prefix_set]
        prefix = entry[7]
        colour_version = entry[10]
        
        # Translate entry
        try:
            if f"{prefix}{track} ({extra})" in json.keys():
                translation = json[f"{prefix}{track} ({extra})"]["translate"][cs.abbreviations[cs.identifiers.index(language)]]
            elif prefix + track in json.keys():
                translation = json[prefix + track]["translate"][cs.abbreviations[cs.identifiers.index(language)]]
            else:
                translation = None
        except KeyError:
            translation = None
        
        total += 1
        if translation is None:
            translation = f"{prefix}{track} ({extra})" if extra else prefix + track
            colour_version += " \\z{800,46}\\c{yor7}(NT)"
            new_prefixes = prefixes
        else:
            new_prefixes = []
            for x, y in zip(prefixes, range(len(prefixes))):
                if x in translation:
                    new_prefixes.append(x)
                    translation = translation.replace(f"{x} ", "")
                else:
                    new_prefixes.append(translation.split(" ")[y])
                    translation = " ".join(translation.split(" ")[1:])
            translated += 1
        
        # Insert information        
        if slot in cs.slot_dict.keys():
            entry[0] = message.replace(slot, cs.slot_dict[slot])
        
        entry[1] = translation
        entry[10] = colour_version
        for prefix, new in zip(prefixes, new_prefixes):
            entry[7] = entry[7].replace(prefix, new)
            entry[9] = entry[9].replace(prefix, new)
        entry[13] = track_type + translation
        
        entries[k] = entry
        
        # Print results
        print(f"Translation of{' ' + ' '.join(prefixes) if prefixes else ''} " +
              f"{track} to {cs.languages[cs.identifiers.index(language)]} is" +
              f"{' ' + ' '.join(new_prefixes) if prefixes else ''} {translation}.")

# Print more results
print(f"Translated {translated} out of {total} names.")
print(f"Translation ratio is {translated / total * 100:.2f}%.")

statistics = fl.TXT(os.path.join(cwd, "Statistics.txt"))
results = f"* {cs.languages[cs.identifiers.index(language)]} - {translated}/{total} ({translated / total * 100:.2f}%)"

if not statistics.exists():
    statistics.write([f"{results}\n"])
else:
    statistics.append(results)

# Insert new translations
entries = [entry if isinstance(entry, str) else "\\n".join(entry) for entry in entries]
translate.write(entries)

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
    translate.copy(os.path.join(patch_dir.path, "bmg", "track-names", file))

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
translate.delete()
force.delete()
tar.delete()
txz.delete()
patch.delete()

input("All done!")