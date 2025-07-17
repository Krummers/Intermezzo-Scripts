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
    
    
    files = fd.get_folder("Files")
    bmgs = fl.TXT(os.path.join(files.path, "bmgs.txt"))
    bmg_file = bmgs.copy(os.path.join(generation.path, "bmgs.txt"))
    bmgs = fl.TXT(bmg_file.path)
    
    return names, authors, versions, slots, musics, tracklist, bmgs

def pulsar_preparation(tracks: list[cm.Track], text_files: tuple[fl.TXT]) -> int:
    """Prepares all text and SZS files for Pulsar."""
    
    names, authors, versions, slots, musics, tracklist, bmgs = text_files
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

def edit_bmgs(arenas: list[cm.Track], text_files: tuple[fl.TXT]) -> dict[str, cm.Track]:
    """Edits the BMGs."""
    
    names, authors, versions, slots, musics, tracklist, bmgs = text_files
    
    # Change "Version created" message
    index = bmgs.find("2847")
    line = bmgs.read()[index]
    line = line[:line.find("=") + 2]
    line += "Intermezzo {date}"
    bmgs.rewrite(index, line, newline = False)
    
    # Fix music speedup message
    index = bmgs.find("4001")
    line = bmgs.read()[index]
    line = line[:line.find("=") + 2]
    line += "Music Speedup"
    bmgs.rewrite(index, line, newline = False)
    
    # Add new messages
    bmgs.append("\n")
    
    # Add Hybrid messages
    bmgs.append("   cea\t= Hybrid")
    bmgs.append(("   ced\t= ■ Drift ■\\n"
                 "Drift lets you take corners without\\n"
               	 "losing speed. There are two drift modes.\\n"
               	 "\\n"
               	 "■ Hybrid Drift ■\\n"
               	 "Drift automatically when turning.\\n"
               	 "Press the drift button for Manual drift with Mini-Turbos.\\n"
               	 "\\n"
               	 "■ Manual Drift ■\\n"
               	 "\\z{802,170000}Hop while turning to drift. Keep\\n"
               	 "drifting to get a Mini-Turbo, which\\n"
               	 "gives you a burst of speed."))
    bmgs.append("   d16\t= Drift both automatically and manually.")
    
    # Add battle arena messages
    used_slots = cs.arena_order.copy()
    for arena in arenas:
        information = arena.get_information()
        
        slot = information["slot"]
        if isinstance(used_slots[slot], cm.Track):
            print(f"{arena} cannot be added because its slot is already in use.")
            continue
        
        used_slots[slot] = arena
    
    for slot, arena in used_slots.items():
        # Continue if slot was not filled
        if not isinstance(arena, cm.Track):
            continue
        
        information = arena.get_information()
        
        identifier = arena.get_identifier()
        c_identifier = arena.get_identifier(colour = True)
        prefix = arena.get_prefix()
        c_prefix = arena.get_prefix(colour = True)
        name = information["name"]
        c_name = information["name"]
        
        name = " ".join(filter(bool, [identifier, prefix, name]))
        c_name = " ".join(filter(bool, [c_identifier, c_prefix, c_name]))
        c_version = information["version"]
        speed = information["speed"]
        
        if speed != 1.0:
            c_version += f" \\c{{off}}\\c{{blue2}}×{speed}"
        
        line = f"   U{cs.arena_order[slot]}\t= {c_name} \\c{{red4}}{c_version}\\c{{off}}"
        bmgs.append(line)
    
    # Add chat messages
    bmgs.append("   M01\t= \\c{blue}Intermezzo {date}\\c{off}")
    bmgs.append("   M02\t= \\c{blue}Host: 0693-2070-4087\\c{off}")
    bmgs.append("   M03\t= \\c{blue}https://discord.gg/PSBBuUa2Qe\\c{off}")
    bmgs.append("   M04\t= \\c{blue}19:30 - 22:30 (CE(S)T)\\c{off}")
    
    bmgs.append("   M05\t= \\c{green}Ten minutes until we begin!\\c{off}")
    bmgs.append("   M06\t= \\c{green}Three minutes until the GP starts!\\c{off}")
    bmgs.append("   M07\t= \\c{green}Let's start this Intermezzo!\\c{off}")
    bmgs.append("   M08\t= \\c{green}Two-minute break for a pee!\\c{off}")
    
    bmgs.append("   M09\t= Is everyone here?")
    bmgs.append("   M10\t= Is everyone ready?")
    bmgs.append("   M11\t= Yes!")
    bmgs.append("   M12\t= No!")
    
    bmgs.append("   M13\t= I am leaving!")
    bmgs.append("   M14\t= Someone else is joining!")
    bmgs.append("   M15\t= Let's do this!")
    bmgs.append("   M16\t= Here we go!")
    
    bmgs.append("   M17\t= So many textures and edits...")
    bmgs.append("   M18\t= We have a battle arena!")
    bmgs.append("   M19\t= I only come for the custom tracks.")
    bmgs.append("   M20\t= I wish there was a wish.")
    
    bmgs.append("   M21\t= CAAAAAAAAAARS!")
    bmgs.append("   M22\t= Tokyo Drift cannon!")
    bmgs.append("   M23\t= Everything about that sucked.")
    bmgs.append("   M24\t= - \\c{red4}-\\c{off} by -")
    
    bmgs.append("   M25\t= Updated sun.")
    bmgs.append("   M26\t= This community keeps surprising me.")
    bmgs.append("   M27\t= Intermassive!")
    bmgs.append("   M28\t= Certified Wiimm moment.")
    
    bmgs.append("   M29\t= Bastard!")
    bmgs.append("   M30\t= Maggot!")
    bmgs.append("   M31\t= Poophead!")
    bmgs.append("   M32\t= Dumbass!")
    
    bmgs.append("   M33\t= Dumb Bullet Bill!")
    bmgs.append("   M34\t= Shitty Shells!")
    bmgs.append("   M35\t= Crappy Mario Kart!")
    bmgs.append("   M36\t= Scheiß Klapsleitung!")
    
    bmgs.append("   M37\t= Will we ever catch up?")
    bmgs.append("   M38\t= The bot stopped working!")
    bmgs.append("   M39\t= I am chat.")
    bmgs.append("   M40\t= Wiimm, our Intermezzo overlord!")
    
    bmgs.append("   M41\t= The 60s crown is mine!")
    bmgs.append("   M42\t= Can you put me in a 1vX?")
    bmgs.append("   M43\t= Nobody can defeat me!")
    bmgs.append("   M44\t= You stole my precious points!")
    
    bmgs.append("   M93\t= \\c{yellow}End Race Early Button Combinations\\c{off}")
    bmgs.append("   M94\t= \\c{yellow}Wiimote: B, +, 1, 2\\c{off}")
    bmgs.append("   M95\t= \\c{yellow}GameCube: L, R, A, Start\\c{off}")
    bmgs.append("   M96\t= \\c{yellow}Classic: L, R, a, +\\c{off}")
    
    return used_slots

def instructions(selection: str, track_counter: int, files: tuple[fl.TXT]) -> None:
    """Prints build instructions for Pulsar."""
    
    print(f"Amount of required cups is {mt.ceil(track_counter / 8) * 2}.")
    print("Drag the track files to the \"/Pulsar/import\" folder.")
    print(f"Name the mod folder name \"{selection}\".")
    
    for file in files:
        os.system(f"start notepad++ \"{file.path}\"")
    
    print(f"Continue once the two folders are in \"/Krummers-Generator/Generations/{selection}\"")

def check_process(selection: str, generation: fl.Folder) -> tuple[fl.Folder, fl.File]:
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
    
    # Add main.dol, Common.szs and arena loader
    file_patch = wiidisc[2]
    dol = et.SubElement(file_patch, "file")
    dol.set("external", f"/{selection}/Codes/main{{$__region}}.dol")
    dol.set("disc", "main.dol")
    dol.set("create", "true")
    
    common = et.SubElement(file_patch, "file")
    common.set("external", f"/{selection}/Items/Common.szs")
    common.set("disc", "Race/Common.szs")
    common.set("create", "true")
    
    arenas = et.SubElement(file_patch, "folder")
    arenas.set("external", f"/{selection}/Arenas")
    arenas.set("disc", "/Race/Course")
    arenas.set("create", "true")
    
    menus = et.SubElement(file_patch, "folder")
    menus.set("external", f"/{selection}/Menus")
    menus.set("disc", "/Scene/UI")
    menus.set("create", "true")
    
    tree = et.ElementTree(wiidisc)
    et.indent(tree, space = "\t")
    tree.write(xml.path)

def add_arenas(arenas: list[cm.Track], selection: str, text_files: tuple[fl.TXT], used_slots: dict[str, cm.Track]) -> None:
    """Adds a maximum of 10 arenas to the distribution."""
    
    if not arenas:
        return
    
    names, authors, versions, slots, musics, tracklist, bmgs = text_files
    tracklist.append(" ")
    
    arena_folder = fl.Folder(os.path.join(os.getcwd(), "Generations", selection, selection, "Arenas"))
    if not bool(arena_folder):
        os.mkdir(arena_folder.path)
    
    # Add arenas to the distribution
    for slot, arena in used_slots.items():
        filename = cs.arena_filenames[slot]
        
        # Continue if slot was not filled
        if not isinstance(arena, cm.Track):
            continue
        
        information = arena.get_information()
        
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
        
        slot_number = cs.arena_order[slot]
        formatted_slot_number = f"A{slot_number[0]}.{slot_number[1]}"
        
        tracklist_string = f" {formatted_slot_number}\t{slot:<8s}{slot:<8s}{name} {version}"
        tracklist_string += f" ({creators})"
        tracklist_string += f" [id={arena.trackid}]"
        tracklist.append(tracklist_string)

def copy_files(mod_folder: fl.Folder) -> None:
    """Copies additional files into a given distribution folder."""
    
    files = fd.get_folder("Files")
    common = fl.File(os.path.join(files.path, "Common.szs"))
    common.copy(os.path.join(mod_folder.path, "Items", common.filename + common.extension))
    
    for region in cs.regions_letters:
        mdol = fl.File(os.path.join(files.path, f"main{region}.dol"))
        
        mdol.copy(os.path.join(mod_folder.path, "Codes", mdol.filename + mdol.extension))

def zip_distribution(selection: str, generation: fl.Folder) -> None:
    """Zips up the two folders of the given distribution."""
    
    zip_file = fl.File(os.path.join(generation.path, f"{selection}.zip"))
    
    os.system(f"7z a \"{zip_file.path}\" \"{os.path.join(generation.path, selection)}\"")
    os.system(f"7z a \"{zip_file.path}\" \"{os.path.join(generation.path, 'riivolution')}\"")

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
    used_arena_slots = edit_bmgs(arenas, text_files)
    instructions(distribution.name, track_counter, text_files)
    
    mod_folder, xml = check_process(distribution.name, generation)
    pulsar_id = get_pulsar_id(xml, distribution.name)
    edit_xml(xml, distribution.name, pulsar_id)
    add_arenas(arenas, distribution.name, text_files, used_arena_slots)
    copy_files(mod_folder)
    
    zip_distribution(distribution.name, generation)

if __name__ == "__main__":
    main()
