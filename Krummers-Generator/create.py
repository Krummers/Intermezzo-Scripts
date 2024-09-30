import os

import common as cm
import folders as fd

import Modules.file as fl

selections = fd.get_folder("Selections")

def select_option(folders: list[str]) -> str:
    """Select what to do for a track selection."""
    
    while True:
        option = input("Create a new track selection, edit an existing one or exit? (N, E or X): ").lower()
        
        if option == "e" and not folders:
            print("There do not exist any selections.")
        elif option == "n":
            return "new"
        elif option == "e":
            return "edit"
        elif option == "x":
            return "exit"
        else:
            print("This is not an option. Please try again.")

def new_selection(folders: list[str]) -> str:
    """Select name for new selection."""
    
    while True:
        print("Only alpha-numeric characters are allowed, as well as dashes.")
        selection = input("What to name this track selection? (Enter the name): ")
        
        if not selection.replace("-", "").replace(" ", "").isalnum():
            print("This name is not alpha-numeric. Please try again.")
            continue
        
        directory = fl.Folder(os.path.join(selections.path, selection))
        if directory.exists():
            print("This name is already in use. Please try again.")
            continue
        
        os.mkdir(directory.path)
        return selection

def save_tracks(selection: str, trackids: list[cm.TrackID]) -> None:
    """Save tracks of a given selection."""
    
    tracks = fl.CFG(os.path.join(selections.path, selection, "tracks.cfg"))
    tracks.set_value(trackids)
    return

def select_action() -> str:
    """Select action to perform on a selection."""
    
    while True:
        option = input("Add tracks, remove tracks, redownload information or exit? (A, R, D or X): ").lower()
        
        if option == "a":
            return "add"
        elif option == "r":
            return "remove"
        elif option == "d":
            return "download"
        elif option == "x":
            return "exit"
        else:
            print("This is not an option. Please try again.")

def select_track_type() -> str:
    """Select type to tie to the track."""
    
    while True:
        option = input("Add tracks normally or as a wish? (N or W): ").lower()
        
        if option == "n":
            return "normal"
        elif option == "w":
            return "wish"
        else:
            print("This is not an option. Please try again.")

def print_trackids(trackids: list[cm.TrackID]) -> None:
    """Print track IDs in a readable way."""
    
    print("Track IDs included:")
    for entry in trackids:
        print(f"{entry.trackid}. {entry.track_type}")
    if not trackids:
        print("\t* (none)")

def trackid_selector(action: str) -> tuple[int]:
    """Select tracks that need to be added/removed."""
    
    if action == "add":
        infinitive = "add"
        present_participle = "adding"
        past_participle = "added"
    elif action == "remove":
        infinitive = "remove"
        present_participle = "removing"
        past_participle = "removed"
        
    print(f"What tracks need to be {past_participle}?")
    print(f"For example, the prompt \"5-9\" will {infinitive} tracks with ID 5, 6, 7, 8 and 9.")
    print(f"{present_participle.capitalize()} a single track is done by entering \"34\".")
    
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
    
    if entry.json.exists() and entry.wbz.exists():
        print(f"Skipping ID {entry.trackid}; files already exist.")
        return
    
    entry.download_json()
    if not entry.json.exists():
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
        if match.wbz.exists():
            match.wbz.delete()
        if match.json.exists():
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
        option = select_option(folders)
        
        if option == "exit":
            return
        
        cm.print_from_list(folders)
        if option == "new":
            selection = new_selection(folders)
        elif option == "edit":
            selection = cm.select_from_list(folders, "Which selection needs to be edited?", print_menu = False)
        
        trackids = cm.load_tracks(selection)
        while True:
            action = select_action()
            
            if action == "exit":
                break
            
            if action == "add":
                track_type = select_track_type()
                print_trackids(trackids)
                first, last = trackid_selector(action)
                trackids = add_trackids(trackids, selection, track_type, first, last)
            elif action == "remove":
                print_trackids(trackids)
                first, last = trackid_selector(action)
                trackids = remove_trackids(trackids, selection, first, last)
            elif action == "download":
                redownload_information(trackids, selection)
        
            save_tracks(selection, trackids)

if __name__ == "__main__":
    main()
