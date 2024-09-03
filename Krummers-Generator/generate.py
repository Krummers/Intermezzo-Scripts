import math as mt
import os

import common as cm
import folders as fd

import Modules.file as fl
import Modules.functions as ft

selections = fd.get_folder("Selections")

def main() -> None:
    folders = fd.get_selections()
    
    selection = cm.select_from_list(folders, "Which selection needs to be generated?")
    
    confirmation = ft.question(f"Are you sure selection \"{selection}\" needs to be generated?")
    if not confirmation:
        return
    
    trackids = sorted(cm.load_tracks(selection))
    generation = fd.make_generation_folder(selection)
    
    names = fl.TXT(os.path.join(generation.path, "names.txt"))
    authors = fl.TXT(os.path.join(generation.path, "authors.txt"))
    versions = fl.TXT(os.path.join(generation.path, "versions.txt"))
    slots = fl.TXT(os.path.join(generation.path, "slots.txt"))
    musics = fl.TXT(os.path.join(generation.path, "musics.txt"))
    tracklist = fl.TXT(os.path.join(generation.path, "tracklist.txt"))
    
    track_counter = 0
    slot_number = cm.Slot(8, 4)
    for x, entry in enumerate(trackids):
        information = entry.get_information()
        track_counter += information["is_track"]
        slot_number += information["is_track"]
        
        if not information["is_track"]:
            continue
        
        entry.szs.filename = f"{x}.szs"
        entry.szs.path = os.path.join(entry.szs.folder, f"{x}.szs")
        entry.convert_szs()
        
        name = information["prefix"]
        if name is not None:
            name += " "
        else:
            name = ""
        name += information["name"]
        if entry.track_type == "wish":
            name = "\\c{blue2}+W\\c{off} " + name
        author = information["author"]
        version = information["version"]
        slot = information["slot"]
        music = information["music"]
        
        names.append(name)
        authors.append(author)
        versions.append(version)
        slots.append(slot)
        musics.append(music)
        tracklist.append(f" {slot_number}\t{slot:<7s}{music:<7s}{name} {version} ({author})")
        if slot_number.track == 4:
            tracklist.append(" ")
    
    if track_counter % 8 != 0:
        for entry in reversed(trackids):
            information = entry.get_information()
            if information["is_track"]:
                slot = information["slot"]
                music = information["music"]
                for x in range(8 - (track_counter % 8)):
                    names.append("-")
                    authors.append("-")
                    versions.append("-")
                    slots.append(slot)
                    musics.append(music)
                break
    
    print(f"Amount of required cups is {mt.ceil(track_counter / 8) * 2}.")
    print("Drag the track files to the \"/Pulsar/import\" folder.")
    for text_file in [names, authors, versions, slots, musics, tracklist]:
        os.system(f"start notepad++ \"{text_file.path}\"")

if __name__ == "__main__":
    main()
