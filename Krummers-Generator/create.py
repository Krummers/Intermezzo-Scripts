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

def print_tracks(distribution: cm.Distribution) -> None:
    """Prints tracks of a distribution."""
    
    print("Track IDs included:")
    string = str(distribution)
    print(string) if string else print("\t* (none)")

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

def download_track(distribution: cm.Distribution, trackid: int,
                   track_type: eb.TrackType) -> None:
    """Downloads a track with given track ID."""
    
    track = cm.Track(trackid, distribution.name, track_type)
    
    # Download track information for the first time
    if not bool(track.json):
        track.download_json()
    
    # If the information does not exist after trying, return
    if not bool(track.json):
        return
    
    if not bool(track.wbz):
        track.download_wbz()
    
    information = track.get_information()
    if information["is_nintendo"] and track.track_type != eb.TrackType.Wish:
        track.track_type = eb.TrackType.Nintendo
    
    distribution.append(track)

def add_tracks(distribution: cm.Distribution, track_type: eb.TrackType,
               first: int, last: int) -> None:
    """Adds a range of tracks to a distribution."""
    
    for trackid in range(first, last + 1):
        track = download_track(distribution, trackid, track_type)
        if track is not None:
            distribution.tracks.append(track)

def remove_tracks(distribution: cm.Distribution, first: int, last: int) -> None:
    """Removes a range of tracks from a distribution."""
    
    for trackid in range(first, last + 1):
        track = distribution.get_track(trackid)
        if track is None:
            print(f"Skipping ID {trackid}; track does not exist.")
            continue
        
        if bool(track.json):
            track.json.delete()
        if bool(track.wbz):
            track.wbz.delete()
        
        distribution.remove(track)

def redownload_information(distribution: cm.Distribution) -> None:
    """Redownloads all track information of a distribution."""
    
    for track in distribution.tracks:
        track.download_json()

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
                ft.print_menu(folders)
                selection = new_selection()
            case "Edit":
                selection = ft.options_question(folders,
                                                "Which selection needs "
                                                "to be edited?")
            case "Exit":
                return
        
        while True:
            distribution = cm.Distribution(selection)
            edit_actions = list(eb.CreateEditAction)
            display = [edit.name for edit in edit_actions]
            edit_action = ft.options_question(edit_actions,
                                              "What action needs to be performed?",
                                              display)
            
            match edit_action.name:
                case "Add":
                    track_types = list((eb.TrackType.Normal, eb.TrackType.Wish))
                    display = [ttype.name for ttype in track_types]
                    track_type = ft.options_question(track_types,
                                                     "What type should the track get?",
                                                     display)
                    print_tracks(distribution)
                    first, last = trackid_selector(edit_action)
                    add_tracks(distribution, track_type, first, last)
                case "Remove":
                    print_tracks(distribution)
                    first, last = trackid_selector(edit_action)
                    remove_tracks(distribution, first, last)
                case "Redownload":
                    redownload_information(distribution)
                case "Exit":
                    break
            
            distribution.save_tracks()

if __name__ == "__main__":
    main()
