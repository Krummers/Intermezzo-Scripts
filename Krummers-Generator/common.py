import json as js
import os

import folders as fd

import Modules.constants as cs
import Modules.file as fl
import Modules.functions as ft

selections = fd.get_folder("Selections")
generations = fd.get_folder("Generations")

class TrackID(object):
    
    def __init__(self, trackid: int, selection: str, track_type = "normal") -> None:
        self.trackid = trackid
        self.selection = selection        
        self.track_type = track_type
        
        self.json = fl.File(os.path.join(selections.path, selection, f"{trackid}.json"))
        self.wbz = fl.File(os.path.join(selections.path, selection, f"{trackid}.wbz"))
        self.szs = fl.File(os.path.join(generations.path, selection, f"{trackid}.szs"))
    
    def __repr__(self) -> str:
        return f"Track ID: {self.trackid}"
    
    def __lt__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        self_data = self.get_information()
        other_data = other.get_information()
        
        if self.track_type == other.track_type:
            return self_data["name"] < other_data["name"]
        
        if self.track_type == "wish":
            return True
        
        if self.track_type == "nintendo":
            if other.track_type == "wish":
                return False
            if other.track_type == "normal":
                return True
        
        if self.track_type == "normal":
            return False
    
    def __le__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        return self < other or self == other
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        return self.trackid == other.trackid and self.track_type == other.track_type
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        return self > other or self == other
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        return not (self <= other)
    
    def __ne__(self, other) -> bool:
        if not isinstance(other, TrackID):
            raise ValueError("'other' must be a TrackID")
        
        return not (self == other)
    
    def download_json(self) -> None:            
        url = f"https://szslibrary.com/api/api.php?id={self.trackid}"
        ft.download(url, self.json.path)
        
        try:
            self.read_json()
        except js.JSONDecodeError:
            print(f"Track ID {self.trackid} is unavailable.")
            self.json.delete()
    
    def download_wbz(self) -> None:
        url = f"https://szslibrary.com/scripts/download.php?id={self.trackid}"
        ft.download(url, self.wbz.path, f"{self.trackid}.wbz")
    
    def convert_szs(self) -> None:
        if not self.wbz.exists():
            raise FileNotFoundError("wbz file does not exist")
        os.system(f"wszst compress --szs {self.wbz.path} --dest={self.szs.path}")
    
    def read_json(self) -> dict:
        if not self.json.exists:
            raise FileNotFoundError("json does not exist")
        
        with open(self.json.path, "r", encoding = "utf-8") as file:
            data = js.load(file)
        
        return data
    
    def get_information(self) -> dict[str, bool | str]:
        if not self.json.exists:
            raise FileNotFoundError("json does not exist")
        
        data = self.read_json()
        information = dict()
        
        information["is_track"] = bool(data["track_info"][0]["track_customtrack"])
        information["is_nintendo"] = bool(data["track_info"][0]["track_nintendo"])
        
        information["prefix"] = data["track_info"][0]["prefix"]
        information["name"] = data["track_info"][0]["trackname"]
        information["author"] = data["track_info"][0]["track_author"]
        information["editor"] = data["track_info"][0]["track_editor"]
        version = data["track_info"][0]["track_version"]
        version_extra = data["track_info"][0]["track_version_extra"]
        if version_extra is not None:
            version += f"-{version_extra}"
        information["version"] = version
        if data["track_info"][0]["track_prop"] is None:
            slot = 8
        else:
            slot = int(data["track_info"][0]["track_prop"])
        information["slot"] = cs.property_slots[f"{slot:#04x}"]
        if data["track_info"][0]["track_music"] is None:
            music = 117
        else:
            music = int(data["track_info"][0]["track_music"])
        information["music"] = cs.music_slots[f"{music:#04x}"]
        
        return information
    
    def get_identifier(self, colour = False) -> str:
        if self.track_type == "normal":
            return
        elif self.track_type == "wish":
            if colour:
                return "\\c{blue2}+W\\c{off}"
            else:
                return "+W"
        elif self.track_type == "nintendo":
            if colour:
                return "\\c{green}+N\\c{off}"
            else:
                return "+N"
    
    def get_prefix(self, colour = False) -> str:
        information = self.get_information()
        prefix = information["prefix"]
        
        if prefix is None:
            return ""
        
        if colour:
            if prefix == "SNES":
                return "\\c{yor7}SNES\\c{off}"
            elif prefix == "N64":
                return "\\c{yor6}N64\\c{off}"
            elif prefix == "GBA":
                return "\\c{yor5}GBA\\c{off}"
            elif prefix == "GCN":
                return "\\c{yor4}GCN\\c{off}"
            elif prefix == "DS":
                return "\\c{yor3}DS\\c{off}"
            elif prefix == "Wii":
                return "\\c{blue1}Wii\\c{off}"
            elif prefix == "3DS":
                return "\\c{yor2}3DS\\c{off}"
            elif prefix == "Wii U" or prefix == "SW":
                return f"\\c{{yor1}}{prefix}\\c{{off}}"
            elif prefix == "Tour":
                return "\\c{yor0}Tour\\c{off}"
            else:
                return f"\\c{{green}}{prefix}\\c{{off}}"
        else:
            return prefix

class Slot(object):
    
    def __init__(self, cup: int, track: int) -> None:
        if track not in range(1, 5):
            raise ValueError("track must be in range(1, 5)")
        self.cup = cup
        self.track = track
    
    def __repr__(self) -> str:
        return str(self)
    
    def __str__(self) -> str:
        return str(self.cup) + "." + str(self.track)
    
    def __add__(self, other):
        if not isinstance(other, int):
            raise TypeError("'other' must be an integer")
        if other < 0:
            raise ValueError("'other' must be non-negative")
        
        result = self
        for _ in range(other):
            result.track += 1
            if result.track > 4:
                result.cup += 1
                result.track = 1
        
        return result

def print_from_list(values: list[str]) -> None:
    for x, value in enumerate(values):
        print(chr(x + 65), ". ", value, sep = "")
    if not values:
        print("\t* (none)")

def select_from_list(values: list[str], question: str, print_menu = True) -> str:
    if not values:
        print("There are no values to select from.")
        return None
    
    if print_menu:
        print_from_list(values)
    
    while True:
        choice = input(f"{question} (Enter the corresponding option): ")
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif ord(choice.upper()) - 65 in range(len(values)):
            return values[ord(choice.upper()) - 65]
        else:
            print("This is not an option. Please try again.")

def load_tracks(selection: str) -> list[TrackID]:
    """Load tracks of a given selection."""
    tracks = fl.CFG(os.path.join(selections.path, selection, "tracks.cfg"))
    trackids = tracks.get_value()
    if trackids is None:
        trackids = []
    return trackids
