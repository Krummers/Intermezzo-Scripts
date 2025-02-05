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
    
    arenas = []
    for x, track in enumerate(tracks):
        information = track.get_information()
        track_counter += information["is_track"]
        slot_counter += information["is_track"]
        
        # If the track is an arena, skip it
        if not information["is_track"]:
            arenas.append(track)
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
                
                return track_counter, arenas
    
    return track_counter, arenas

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
    wiidisc = tree.getroot()
    
    # Add performance monitor option
    performance_option = et.SubElement(wiidisc[1][0], "option")
    performance_option.set("name", "Performance Monitor")
    choice = et.SubElement(performance_option, "choice")
    choice.set("name", "Enabled")
    patch = et.SubElement(choice, "patch")
    patch.set("id", f"{selection}{pulsarid}PerfMon")
    
    # Add main.dol, Common.szs and arena loader
    file_patch = wiidisc[2]
    dol = et.SubElement(file_patch, "file")
    dol.set("external", f"/{selection}/Codes/main{{$__region}}.dol")
    dol.set("disc", "/main.dol")
    dol.set("create", "true")
    
    common = et.SubElement(file_patch, "file")
    common.set("external", f"/{selection}/Items/Common.szs")
    common.set("disc", "/Race/Common.szs")
    common.set("create", "true")
    
    arenas = et.SubElement(file_patch, "folder")
    arenas.set("external", f"/{selection}/Arenas")
    arenas.set("disc", "/Race/Course")
    arenas.set("create", "true")
    
    menus = et.SubElement(file_patch, "folder")
    menus.set("external", f"/{selection}/Menus")
    menus.set("disc", "/Scene/UI")
    menus.set("create", "true")
    
    # Add performance monitor main.dol loader
    perf_loader = et.SubElement(wiidisc, "patch")
    perf_loader.set("id", f"{selection}{pulsarid}PerfMon")
    
    perf_dol = et.SubElement(perf_loader, "file")
    perf_dol.set("external", f"/{selection}/Codes/perf{{$__region}}.dol")
    perf_dol.set("disc", "/main.dol")
    perf_dol.set("create", "true")
    
    tree = et.ElementTree(wiidisc)
    et.indent(tree, space = "\t")
    tree.write(xml.path)

def add_arenas(arenas: list[cm.Track], selection: str, text_files: tuple[fl.TXT]) -> None:
    """Adds a maximum of 10 arenas to the distribution."""
    
    if not arenas:
        return
    
    names, authors, versions, slots, musics, tracklist = text_files
    tracklist.append(" ")
    
    arena_folder = fl.Folder(os.path.join(os.getcwd(), "Generations", selection, selection, "Arenas"))
    if not bool(arena_folder):
        os.mkdir(arena_folder.path)
    
    # Extract text files for BMGs
    for language in cs.languages:
        szs = fl.File(os.path.join(os.getcwd(), "Files", f"MenuSingle_{language}.szs"))
        copied_szs = szs.copy(os.path.join(os.getcwd(), "Generations", selection, f"MenuSingle_{language}.szs"))
        extracted_file = fl.Folder(os.path.join(os.getcwd(), "Generations", selection, f"MenuSingle_{language}.d"))
        bmg = fl.File(os.path.join(extracted_file.path, "message", "Common.bmg"))
        
        os.system(f"wszst extract \"{copied_szs.path}\"")
        os.system(f"wbmgt decode \"{bmg.path}\"")
    
    slot_counter = cm.Slot(1, 1, arena = True)
    used_slots = set()
    for arena in arenas:
        information = arena.get_information()
        
        slot = information["slot"]
        if slot in used_slots:
            print(f"{arena} cannot be added because its slot is already in use.")
            continue
        
        slot_counter += 1
        used_slots.add(slot)
        filename = cs.arena_filenames[slot]
        
        arena.szs.filename = filename
        arena.szs.path = os.path.join(arena.szs.folder, selection, "Arenas", f"{filename}.szs")
        arena.convert_szs()
        
        identifier = arena.get_identifier()
        c_identifier = arena.get_identifier(colour = True)
        prefix = arena.get_prefix()
        c_prefix = arena.get_prefix(colour = True)
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
        
        for language in cs.languages:
            extracted_file = fl.Folder(os.path.join(os.getcwd(), "Generations", selection, f"MenuSingle_{language}.d"))
            text = fl.TXT(os.path.join(extracted_file.path, "message", "Common.txt"))
            
            index = text.find(f"U{cs.arena_order[slot]}")
            
            # Edge case for French (NTSC-U)
            if language == "Q" and slot == "arS":
                index = text.find("24c1")
            
            line = text.read()[index]
            new_line = line[:line.find("=") + 2]
            new_line += f"{c_name} {c_version}"
            
            text.rewrite(index, new_line, newline = False)
        
        tracklist_string = f" {slot_counter}\t{slot:<8s}{slot:<8s}{name} {version}"
        tracklist_string += f" ({creators})"
        tracklist_string += f" [id={arena.trackid}]"
        tracklist.append(tracklist_string)
        
        if slot_counter.track == 5:
            tracklist.append(" ")
    
    # Create new BMGs and add them to the distribution
    for language in cs.languages:
        copied_szs = szs.copy(os.path.join(os.getcwd(), "Generations", selection, f"MenuSingle_{language}.szs"))
        extracted_file = fl.Folder(os.path.join(os.getcwd(), "Generations", selection, f"MenuSingle_{language}.d"))
        text = fl.TXT(os.path.join(extracted_file.path, "message", "Common.txt"))
        
        os.system(f"wbmgt encode \"{text.path}\" -o")
        text.delete()
        os.system(f"wszst create \"{extracted_file.path}\" -o")
        extracted_file.delete()
        copied_szs.move_down([selection, "Menus"])

def copy_files(mod_folder: fl.Folder) -> None:
    """Copies additional files into a given distribution folder."""
    
    files = fd.get_folder("Files")
    common = fl.File(os.path.join(files.path, "Common.szs"))
    common.copy(os.path.join(mod_folder.path, "Items", common.filename))
    
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
    
    track_counter, arenas = pulsar_preparation(tracks, text_files)
    instructions(distribution.name, track_counter, text_files)
    
    mod_folder, xml = check_process(distribution.name, generation)
    pulsar_id = get_pulsar_id(xml, distribution.name)
    edit_xml(xml, distribution.name, pulsar_id)
    add_arenas(arenas, selection, text_files)
    copy_files(mod_folder)

if __name__ == "__main__":
    main()
