import math as mt
import os
import script_utilities.file as fl
import script_utilities.functions as ft
import xml.etree.ElementTree as et

import common as cm
import folders as fd

import Modules.constants as cs

selections = fd.get_folder("Selections")

def create_text_files(generation: fl.Folder) -> list[fl.TXT]:
    """Creates text files for Pulsar's mass import."""
    
    names = fl.TXT(os.path.join(generation.path, "names.txt"))
    authors = fl.TXT(os.path.join(generation.path, "authors.txt"))
    versions = fl.TXT(os.path.join(generation.path, "versions.txt"))
    slots = fl.TXT(os.path.join(generation.path, "slots.txt"))
    musics = fl.TXT(os.path.join(generation.path, "musics.txt"))
    tracklist = fl.TXT(os.path.join(generation.path, "tracklist.txt"))
    return names, authors, versions, slots, musics, tracklist

def pulsar_preparation(tracks: list[cm.Track], text_files: tuple[fl.TXT]) -> int:
    """Prepares all text and SZS files for Pulsar."""
    
    names, authors, versions, slots, musics, tracklist = text_files
    track_counter = 0
    slot_counter = cm.Slot(8, 4)
    
    for x, track in enumerate(tracks):
        information = track.get_information()
        track_counter += information["is_track"]
        slot_counter += information["is_track"]
        
        # If the track is an arena, skip it
        if not information["is_track"]:
            continue
        
        track.szs.filename = str(x)
        track.szs.path = os.path.join(track.szs.folder, f"{x}.szs")
        track.convert_szs()
        
        identifier = track.get_identifier()
        c_identifier = track.get_identifier(colour = True)
        prefix = track.get_prefix()
        c_prefix = track.get_prefix(colour = True)
        name = information["name"]
        c_name = information["name"]
        
        name = " ".join(filter(bool, [identifier, prefix, name]))
        c_name = " ".join(filter(bool, [c_identifier, c_prefix, c_name]))
        
        creators = ",,".join(filter(bool, [information["author"], information["editor"]]))
        
        version = information["version"]
        c_version = information["version"]
        speed = information["speed"]
        
        if speed != 1.0:
            c_version += f" \\c{{off}}\\c{{blue2}}×{speed}"
        
        slot = information["slot"]
        music = information["music"]
        
        names.append(c_name)
        authors.append(creators)
        versions.append(c_version)
        slots.append(slot)
        musics.append(music)
        
        tracklist_string = f" {slot_counter}\t{slot:<8s}{music:<8s}{name} {version}"
        tracklist_string += f" ({creators})"
        tracklist_string += f" [id={track.trackid}]"
        tracklist.append(tracklist_string)
        if slot_counter.track == 4:
            tracklist.append(" ")
    
    if track_counter % 8 != 0:
        for track in reversed(tracks):
            information = track.get_information()
            
            if information["is_track"]:
                slot = information["slot"]
                music = information["music"]
                
                for y in range(8 - (track_counter % 8)):
                    names.append("-")
                    authors.append("-")
                    versions.append("-")
                    slots.append(slot)
                    musics.append(music)
                    
                    szs = fl.File(os.path.join(track.szs.folder, f"{x}.szs"))
                    x += 1
                    szs.copy(os.path.join(track.szs.folder, f"{x}.szs"))
                
                return track_counter
    return track_counter

def instructions(selection: str, track_counter: int, files: list[fl.TXT]) -> None:
    """Prints build instructions for Pulsar."""
    
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
        
        if bool(mod_folder) and bool(xml):
            return mod_folder, xml
    
        print("The folders do not exist yet.")

def get_pulsar_id(xml: fl.File, selection: str) -> str:
    """Extracts a randomly gerenated Pulsar ID from a given XML."""
    
    tree = et.parse(xml.path)
    root = tree.getroot()
    packid = root[1][0][0][0][0].get("id")
    pulsar_id = packid.replace(selection, "").replace("LoadPack", "")
    return pulsar_id

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
    # root[2].append(et.Element("file"))
    # root[2][-1].set("external", f"/{selection}/Items/Common.szs")
    # root[2][-1].set("disc", "Race/Common.szs")
    # root[2][-1].set("create", "true")
    # root[2][-1].tail = "\n\t"
    
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
    # common = fl.File(os.path.join(files.path, "Common.szs"))
    # common.copy(os.path.join(mod_folder.path, "Items", common.filename))
    
    for region in cs.regions_letters:
        mdol = fl.File(os.path.join(files.path, f"main{region}.dol"))
        pdol = fl.File(os.path.join(files.path, f"perf{region}.dol"))
        
        mdol.copy(os.path.join(mod_folder.path, "Codes", mdol.filename + mdol.extension))
        pdol.copy(os.path.join(mod_folder.path, "Codes", pdol.filename + pdol.extension))

def main() -> None:
    folders = fd.get_selections()
    selection = ft.options_question(folders, "Which selection needs to be generated?")
    confirmation = ft.question(f"Are you sure selection \"{selection}\" needs to be generated?")
    if not confirmation:
        return
    
    distribution = cm.Distribution(selection)
    tracks = sorted(distribution.tracks)
    generation = fd.make_generation_folder(distribution.name)
    text_files = create_text_files(generation)
    
    track_counter = pulsar_preparation(tracks, text_files)
    instructions(distribution.name, track_counter, text_files)
    
    mod_folder, xml = check_process(distribution.name, generation)
    pulsar_id = get_pulsar_id(xml, distribution.name)
    edit_xml(xml, distribution.name, pulsar_id)
    copy_files(mod_folder)

if __name__ == "__main__":
    main()
