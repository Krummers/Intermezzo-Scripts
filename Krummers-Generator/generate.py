import math as mt
import os
import xml.etree.ElementTree as et

import common as cm
import folders as fd

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

selections = fd.get_folder("Selections")

def create_text_files(generation: fl.Folder) -> list[fl.TXT]:
    """Create text files for Pulsar mass import."""
    
    names = fl.TXT(os.path.join(generation.path, "names.txt"))
    authors = fl.TXT(os.path.join(generation.path, "authors.txt"))
    versions = fl.TXT(os.path.join(generation.path, "versions.txt"))
    slots = fl.TXT(os.path.join(generation.path, "slots.txt"))
    musics = fl.TXT(os.path.join(generation.path, "musics.txt"))
    tracklist = fl.TXT(os.path.join(generation.path, "tracklist.txt"))
    return names, authors, versions, slots, musics, tracklist

def generation_loop(trackids: list[cm.TrackID], files: tuple[fl.TXT]) -> int:
    """Main loop for generating the track list, BMGs and files."""
    names, authors, versions, slots, musics, tracklist = files
    track_counter = 0
    slot_number = cm.Slot(8, 4)
    
    for x, entry in enumerate(trackids):
        information = entry.get_information()
        track_counter += information["is_track"]
        slot_number += information["is_track"]
        
        if not information["is_track"]:
            # handle arenas here
            continue
        
        entry.szs.filename = f"{x}.szs"
        entry.szs.path = os.path.join(entry.szs.folder, f"{x}.szs")
        entry.convert_szs()
        
        identifier = entry.get_identifier()
        c_identifier = entry.get_identifier(colour = True)
        name = entry.get_prefix()
        c_name = entry.get_prefix(colour = True)
        
        speed = information["speed"]
        
        if name != "":
            name += " "
            c_name += " "
        else:
            name = ""
            c_name = ""
        name += information["name"]
        c_name += information["name"]
        if identifier is not None:
            name = f"{identifier} {name}"
            c_name = f"{c_identifier} {c_name}"
        
        author = information["author"]
        editor = information["editor"]
        
        version = information["version"]
        c_version = information["version"]
        if information["speed"] != 1.0:
            c_version += f" \\c{{off}}\\c{{blue2}}×{speed}"
        
        slot = information["slot"]
        music = information["music"]
        
        names.append(c_name)
        if editor is not None:
            authors.append(f"{author},,{editor}")
        else:
            authors.append(author)
        versions.append(c_version)
        slots.append(slot)
        musics.append(music)
        
        string = f" {slot_number}\t{slot:<8s}{music:<8s}{name} {version}"
        if editor is not None:
            string += f" ({author},,{editor})"
        else:
            string += f" ({author})"
        string += f" [id={entry.trackid}]"
        tracklist.append(string)
        if slot_number.track == 4:
            tracklist.append(" ")
    
    if track_counter % 8 != 0:
        for entry in reversed(trackids):
            information = entry.get_information()
            if information["is_track"]:
                slot = information["slot"]
                music = information["music"]
                for y in range(8 - (track_counter % 8)):
                    names.append("-")
                    authors.append("-")
                    versions.append("-")
                    slots.append(slot)
                    musics.append(music)
                    last_szs = fl.File(os.path.join(entry.szs.folder, f"{x}.szs"))
                    x += 1
                    last_szs.copy(os.path.join(entry.szs.folder, f"{x}.szs"))
                return track_counter
    return track_counter

def instructions(selection: str, track_counter: int, files: list[fl.TXT]) -> None:
    """Print instructions for Pulsar."""
    
    print(f"Amount of required cups is {mt.ceil(track_counter / 8) * 2}.")
    print("Drag the track files to the \"/Pulsar/import\" folder.")
    print(f"Name the mod folder name \"{selection}\".")
    
    for file in files:
        os.system(f"start notepad++ \"{file.path}\"")
    
    print(f"Continue once the two folders are in \"/Krummers-Generator/Generations/{selection}\"")

def check_process(selection: str, generation: fl.File) -> tuple[fl.Folder, fl.File]:
    """Checks if the Pulsar-generated distribution has been placed correctly."""
    
    mod_folder = fl.Folder(os.path.join(generation.path, selection))
    xml = fl.File(os.path.join(generation.path, "riivolution", f"{selection}.xml"))
    
    while True:
        continue_process = ft.question("Continue process?")
        
        if not continue_process:
            continue
        
        if mod_folder.exists() and xml.exists():
            return mod_folder, xml
    
        print("The folders do not exist yet.")

def get_pulsar_id(xml: fl.File, selection: str) -> str:
    """Extracts randomly gerenated Pulsar ID from a given XML."""
    
    tree = et.parse(xml.path)
    root = tree.getroot()
    packid = root[1][0][0][0][0].get("id")
    pulsarid = packid.replace(selection, "").replace("LoadPack", "")
    return pulsarid

def edit_xml(xml: fl.File, selection: str, pulsarid: str) -> None:
    """Modifies a given XML to let Riivolution read from the correct locations."""
    
    tree = et.parse(xml.path)
    root = tree.getroot()
    
    # Add performance monitor option
    root[1][0].append(et.Element("option"))
    root[1][0][1].tail = "\n\t\t\t"
    root[1][0][2].set("name", "Performance Monitor")
    root[1][0][2].text = "\n\t\t\t\t"
    root[1][0][2].tail = "\n\t\t"
    root[1][0][2].append(et.Element("choice"))
    root[1][0][2][0].set("name", "Enabled")
    root[1][0][2][0].text = "\n\t\t\t\t\t"
    root[1][0][2][0].tail = "\n\t\t\t"
    root[1][0][2][0].append(et.Element("patch"))
    root[1][0][2][0][0].set("id", f"{selection}{pulsarid}PerfMon")
    root[1][0][2][0][0].tail = "\n\t\t\t\t"
    
    # Add main.dol and Common.szs loader
    root[2][-1].tail = "\n\t\t"
    root[2].append(et.Element("file"))
    root[2][-1].set("external", f"/{selection}/Codes/main{{$__region}}.dol")
    root[2][-1].set("disc", "main.dol")
    root[2][-1].set("create", "true")
    root[2][-1].tail = "\n\t\t"
    root[2].append(et.Element("file"))
    root[2][-1].set("external", f"/{selection}/Items/Common.szs")
    root[2][-1].set("disc", "Race/Common.szs")
    root[2][-1].set("create", "true")
    root[2][-1].tail = "\n\t"
    
    # Add performance monitor main.dol loader
    root[-1].tail = "\n\t"
    root.append(et.Element("patch"))
    root[-1].set("id", f"{selection}{pulsarid}PerfMon")
    root[-1].text = "\n\t\t"
    root[-1].append(et.Element("file"))
    root[-1][0].set("external", f"/{selection}/Codes/perf{{$__region}}.dol")
    root[-1][0].set("disc", "main.dol")
    root[-1][0].set("create", "true")
    root[-1][0].tail = "\n\t"
    root[-1].tail = "\n"
    
    tree.write(xml.path)

def copy_files(mod_folder: fl.Folder) -> None:
    """Copies additional files into a given distribution folder."""
    
    files = fd.get_folder("Files")
    common = fl.File(os.path.join(files.path, "Common.szs"))
    common.copy(os.path.join(mod_folder.path, "Items", common.filename))
    
    for region in cs.regions_letters:
        mdol = fl.File(os.path.join(files.path, f"main{region}.dol"))
        pdol = fl.File(os.path.join(files.path, f"perf{region}.dol"))
        
        mdol.copy(os.path.join(mod_folder.path, "Codes", mdol.filename))
        pdol.copy(os.path.join(mod_folder.path, "Codes", pdol.filename))

def main() -> None:
    folders = fd.get_selections()
    selection = cm.select_from_list(folders, "Which selection needs to be generated?")
    confirmation = ft.question(f"Are you sure selection \"{selection}\" needs to be generated?")
    if not confirmation:
        return
    
    trackids = sorted(cm.load_tracks(selection))
    generation = fd.make_generation_folder(selection)
    files = create_text_files(generation)
    
    track_counter = generation_loop(trackids, files)
    instructions(selection, track_counter, files)
    
    mod_folder, xml = check_process(selection, generation)
    pulsarid = get_pulsar_id(xml, selection)
    edit_xml(xml, selection, pulsarid)
    copy_files(mod_folder)

if __name__ == "__main__":
    main()
