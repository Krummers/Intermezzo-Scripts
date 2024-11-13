import os
import script_utilities.file as fl
import script_utilities.functions as ft

import common as cm
import folders as fd

import Modules.enumerables as eb

selections = fd.get_folder("Selections")

def new_selection() -> str:
    """Lets the user enter a name for a new selection."""
    
    while True:
        print("Only alpha-numeric characters are allowed, as well as dashes.")
        selection = input("What to name this track selection? (Enter the name): ")
        
        if not selection.replace("-", "").isalnum():
            print("This name is not alpha-numeric. Please try again.")
            continue
        
        directory = fl.Folder(os.path.join(selections.path, selection))
        if bool(directory):
            print("This name is already in use. Please try again.")
            continue
        
        os.mkdir(directory.path)
        return selection

def save_tracks(selection: str, trackids: list[cm.TrackID]) -> None:
    """Saves a list of tracks to a given selection."""
    
    tracks = fl.PKL(os.path.join(selections.path, selection, "tracks.pkl"))
    tracks.set_value(trackids)
    return

def print_trackids(trackids: list[cm.TrackID]) -> None:
    """Print track IDs in a readable way."""
    
    print("Track IDs included:")
    for entry in trackids:
        print(f"{entry.trackid}. {entry.track_type}")
    if not trackids:
        print("\t* (none)")

def trackid_selector(action: eb.CreateEditAction) -> tuple[int]:
    """Lets the user select a range of tracks."""
    
    match action.name:
        case "Add":
            infinitive = "add"
            present_participle = "adding"
            past_participle = "added"
        case "Remove":
            infinitive = "remove"
            present_participle = "removing"
            past_participle = "removed"
        
    print(f"What tracks need to be {past_participle}?")
    print(f"For example, the prompt \"5-9\" will {infinitive} tracks "
          "with ID 5, 6, 7, 8 and 9.")
    print(f"{present_participle.capitalize()} a single track is done "
          "by entering \"34\".")
    
    while True:
        prompt = input("Enter the first and last track ID separated by a dash or a single ID on its own: ")
        
        try:
            prompt = prompt.split("-")
            
            if len(prompt) == 1:
                first, last = int(prompt[0]), int(prompt[0])
            elif len(prompt) == 2:
                first, last = int(prompt[0]), int(prompt[1])
            else:
                raise ValueError
        except ValueError:
            print("This prompt was not properly formatted. Please try again.")
            continue
        
        if last < first:
            first, last = last, first
        
        return first, last

def trackid_downloader(trackid: int, selection: str, track_type: str) -> cm.TrackID | None:
    """Download a given track for a certain selection."""
    
    entry = cm.TrackID(trackid, selection, track_type)
    
    if bool(entry.json) and bool(entry.wbz):
        print(f"Skipping ID {entry.trackid}; files already exist.")
        return
    
    entry.download_json()
    if not bool(entry.json):
        return None
    
    # Mark as Nintendo track when needed
    information = entry.get_information()
    if information["is_nintendo"] and entry.track_type != "wish":
        entry.track_type = "nintendo"
    
    entry.download_wbz()
    return entry

def add_trackids(trackids: list[cm.TrackID], selection: str, track_type: str, first: int, last: int) -> list[cm.TrackID]:
    """Add track IDs to track selection."""
    
    for trackid in range(first, last + 1):
        entry = trackid_downloader(trackid, selection, track_type)
        if entry is not None:
            trackids.append(entry)
    return trackids

def remove_trackids(trackids: list[cm.TrackID], selection: str, first: int, last: int) -> list[cm.TrackID]:
    """Remove track IDs from track selection."""
    
    for trackid in range(first, last + 1):
        matches = [trackid == entry.trackid for entry in trackids]
        if not any(matches):
            print(f"Skipping ID {trackid}; track does not exist.")
            continue
        
        match = trackids[matches.index(True)]
        
        print(f"Removing ID {trackid}...")        
        if bool(match.wbz):
            match.wbz.delete()
        if bool(match.json):
            match.json.delete()
        
        trackids.remove(match)
    
    return trackids

def redownload_information(trackids: list[cm.TrackID], selection: str) -> None:
    """Redownload JSON for every track ID."""
    
    for trackid in trackids:
        print(f"Redownloading information from track ID {trackid.trackid}...")
        trackid.download_json()

def main() -> None:
    while True:
        folders = fd.get_selections()
        actions = list(eb.CreateAction)
        display = [action.name for action in actions]
        action = ft.options_question(actions,
                                     "What action needs to be performed?",
                                     display)
        
        match action.name:
            case "Create":
                cm.print_from_list(folders)
                selection = new_selection()
            case "Edit":
                cm.print_from_list(folders)
                selection = cm.select_from_list(folders,
                                                "Which selection needs "
                                                "to be edited?",
                                                print_menu = False)
            case "Exit":
                return
        
        trackids = cm.load_tracks(selection)
        while True:
            edit_actions = list(eb.CreateEditAction)
            display = [edit.name for edit in edit_actions]
            edit_action = ft.options_question(edit_actions,
                                              "What action needs to be performed?",
                                              display)
            
            match edit_action.name:
                case "Add":
                    track_types = list(eb.TrackType)[:-1]
                    display = [ttype.name for ttype in track_types]
                    track_type = ft.options_question(track_types,
                                                     "What type should the track get?",
                                                     display)
                    print_trackids(trackids)
                    first, last = trackid_selector(edit_action)
                    trackids = add_trackids(trackids, selection, track_type, first, last)
                case "Remove":
                    print_trackids(trackids)
                    first, last = trackid_selector(edit_action)
                    trackids = remove_trackids(trackids, selection, first, last)
                case "Redownload":
                    redownload_information(trackids, selection)
                case "Exit":
                    break
            
            save_tracks(selection, trackids)

if __name__ == "__main__":
    main()
