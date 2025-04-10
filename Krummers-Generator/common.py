import json as js
import os
import script_utilities.date as dt
import script_utilities.file as fl
import script_utilities.functions as ft
import typing as tp

import folders as fd

import Modules.constants as cs
import Modules.enumerables as eb

selections = fd.get_folder("Selections")
generations = fd.get_folder("Generations")

class Track(object):
    
    def __init__(self, trackid: int, selection: str,
                 track_type: eb.TrackType = eb.TrackType.Normal) -> None:
        if not isinstance(trackid, int):
            raise TypeError("unsupported type for trackid: "
                            f"'{type(trackid).__name__}'")
        
        if not isinstance(selection, str):
            raise TypeError("unsupported type for selection: "
                            f"'{type(selection).__name__}'")
        
        if not isinstance(track_type, eb.TrackType):
            raise TypeError("unsupported type for track_type: "
                            f"'{type(track_type).__name__}'")
        
        self.trackid = trackid
        self.selection = selection
        self.track_type = track_type
        
        self.json = fl.File(os.path.join(selections.path, selection, f"{trackid}.json"))
        self.wbz = fl.File(os.path.join(selections.path, selection, f"{trackid}.wbz"))
        self.szs = fl.File(os.path.join(generations.path, selection, f"{trackid}.szs"))
    
    def __repr__(self) -> str:
        """Represents the object in a console."""
        
        return f"Track[ID={self.trackid}]"
    
    def __str__(self) -> str:
        """Returns the track ID, type and name."""
        
        information = self.get_information()
        name = information["name"]
        version = information["version"]
        prefix = self.get_prefix()
        
        string = f"{self.trackid}. {self.track_type.name}"
        string += f" [{prefix} " if prefix else " ["
        string += f"{name} {version}]"
        return string
    
    def __lt__(self, other: tp.Self) -> bool:
        if not isinstance(other, Track):
            raise TypeError("unsupported operand type(s) for '<': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        self_data = self.get_information()
        other_data = other.get_information()
        
        if self.track_type != other.track_type:
            return self.track_type < other.track_type
        
        if self_data["name"] != other_data["name"]:
            return self_data["name"].lower() < other_data["name"].lower()
        
        if self_data["prefix"] != other_data["prefix"]:
            return self_data["prefix"].lower() < other_data["prefix"].lower()
        
        if self_data["date"] != other_data["date"]:
            self_date = dt.Date(*map(int, self_data["date"].split("-")))
            other_date = dt.Date(*map(int, other_data["date"].split("-")))
            return self_date < other_date
        
        return False
    
    def __le__(self, other) -> bool:
        if not isinstance(other, Track):
            raise TypeError("unsupported operand type(s) for '<=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self < other or self == other
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Track):
            return False
        
        return self.trackid == other.trackid and self.track_type == other.track_type
    
    def __ge__(self, other) -> bool:
        if not isinstance(other, Track):
            raise TypeError("unsupported operand type(s) for '>=': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return self > other or self == other
    
    def __gt__(self, other) -> bool:
        if not isinstance(other, Track):
            raise TypeError("unsupported operand type(s) for '>': "
                            f"'{type(self).__name__}' and '{type(other).__name__}'")
        
        return not (self <= other)
    
    def __ne__(self, other) -> bool:
        if not isinstance(other, Track):
            return True
        
        return self.trackid != other.trackid or self.track_type != other.track_type
    
    def download_json(self) -> None:
        """Downloads the JSON of the track."""
        
        url = f"https://szslibrary.com/api/api.php?id={self.trackid}"
        ft.download(url, self.json.path, progress = False,
                    description = f"{self.trackid}.json")
        
        try:
            self.read_json()
        except js.JSONDecodeError:
            print(f"Track ID {self.trackid} is unavailable.")
            self.json.delete()
    
    def download_wbz(self) -> None:
        """Downloads the WBZ of the track."""
        
        url = f"https://szslibrary.com/scripts/download.php?id={self.trackid}"
        ft.download(url, self.wbz.path, progress = True,
                    description = f"{self.trackid}.wbz")
    
    def convert_szs(self) -> None:
        """Converts the WBZ of the track to an SZS."""
        
        if not bool(self.wbz):
            raise FileNotFoundError("The system cannot find the file specified: "
                                    f"'{self.wbz.path}'")
            
        os.system(f"wszst compress --szs \"{self.wbz.path}\" "
                  f"--dest=\"{self.szs.path}\"")
    
    def read_json(self) -> dict:
        """Returns all the data found in the JSON of the track."""
        
        if not bool(self.json):
            raise FileNotFoundError("The system cannot find the file specified: "
                                    f"'{self.json.path}'")
        
        with open(self.json.path, "r", encoding = "utf-8") as file:
            data = js.load(file)
        
        return data
    
    def get_information(self) -> dict[str, bool | str]:
        """Returns part of the data of the track in a dictionary."""
        
        if not bool(self.json):
            raise FileNotFoundError("The system cannot find the file specified: "
                                    f"'{self.json.path}'")
        
        data = self.read_json()
        information = dict()
        
        information["is_track"] = bool(data["track_info"][0]["track_customtrack"])
        information["is_nintendo"] = bool(data["track_info"][0]["track_nintendo"])
        
        prefix = data["track_info"][0]["prefix"]
        information["prefix"] = prefix if prefix else ""
        information["name"] = data["track_info"][0]["trackname"]
        information["author"] = data["track_info"][0]["track_author"]
        editor = data["track_info"][0]["track_editor"]
        information["editor"] = editor if editor else ""
        version = data["track_info"][0]["track_version"]
        version_extra = data["track_info"][0]["track_version_extra"]
        
        if version_extra == "":
            version_extra = None
        
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
        
        information["sha1"] = data["track_info"][0]["track_sha1"]
        information["date"] = data["track_info"][0]["track_created"]
        speed = data["track_info"][0]["track_speed"]
        information["speed"] = float(speed) if speed else 1.0
        laps = data["track_info"][0]["track_laps"]
        information["laps"] = int(laps) if laps else 3
        
        return information
    
    def get_identifier(self, colour = False) -> str:
        """Returns the identifier of the track for the BMG."""
        
        match self.track_type.name:
            case "Normal":
                return ""
            case "Wish":
                return "\\c{blue2}+W\\c{off}" if colour else "+W"
            case "Nintendo":
                return "\\c{green}+N\\c{off}" if colour else "+N"
    
    def get_prefix(self, colour = False) -> str:
        """Returns the prefix of the track for the BMG."""
        
        information = self.get_information()
        prefix = information["prefix"]
        
        if prefix is None:
            return ""
        
        if not colour:
            return prefix
        
        for spaced_prefix in ["Spyro 1", "Wii U", "TLoZ ALttP",
                              "TLoZ OoT", "TLoZ TP", "TLoZ TWW"]:
            prefix = prefix.replace(spaced_prefix, spaced_prefix.replace(" ", "|"))
        
        prefixes = prefix.split()
        prefixes = [prefix.replace("|", " ") for prefix in prefixes]
        for x, prefix in enumerate(prefixes):
            match prefix:
                case "SNES":
                    prefixes[x] = "\\c{red4}SNES\\c{off}"
                case "N64":
                    prefixes[x] = "\\c{yellow}N64\\c{off}"
                case "GBA":
                    prefixes[x] = "\\c{yor4}GBA\\c{off}"
                case "GCN":
                    prefixes[x] = "\\c{green}GCN\\c{off}"
                case "DS":
                    prefixes[x] = "\\c{blue2}DS\\c{off}"
                case "Wii":
                    prefixes[x] = "\\c{blue1}Wii\\c{off}"
                case "3DS":
                    prefixes[x] = "\\c{yor2}3DS\\c{off}"
                case "Wii U" | "SW" | "MK8DX":
                    prefixes[x] = f"\\c{{yor6}}{prefix}\\c{{off}}"
                case "Tour" | "RMX":
                    prefixes[x] = f"\\c{{red1}}{prefix}\\c{{off}}"
                case _:
                    prefixes[x] = f"\\c{{green}}{prefix}\\c{{off}}"
        
        return " ".join(prefixes)

class Distribution(object):
    
    def __init__(self, selection: str) -> None:
        if not isinstance(selection, str):
            raise TypeError("unsupported type for selection: "
                            f"'{type(selection).__name__}'")
        
        self.name = selection
        self.pickle = fl.PKL(os.path.join(selections.path, selection, "tracklist.pkl"))
        self.tracks = []
        
        self.load_tracks()        
    
    def __repr__(self) -> str:
        """Represents the object in a console."""
        
        return f"{self.name}[Tracks={len(self.tracks)}]"
    
    def __str__(self) -> str:
        """Returns the tracklist sorted by track ID."""
        
        tracks = sorted(self.tracks, key = lambda track:track.trackid)
        return "\n".join([str(track) for track in tracks])
    
    def load_tracks(self) -> None:
        """Loads all tracks in the file."""
        
        self.tracks = []
        
        if (tracklist := self.pickle.get_value()) is not None:
            for track in tracklist:
                track = Track(track[0], self.name, track[1])
                self.tracks.append(track)
    
    def save_tracks(self) -> None:
        """Saves all tracks to the file."""
        
        tracks = []
        
        for track in sorted(self.tracks, key = lambda track:track.trackid):
            tracks.append((track.trackid, track.track_type))
        
        self.pickle.set_value(tracks)
    
    def append(self, track: Track) -> None:
        """Adds a track to the distribution."""
        
        if not isinstance(track, Track):
            raise TypeError("unsupported type for track: "
                            f"'{type(track).__name__}'")
        
        self.tracks.append(track)
    
    def remove(self, track: Track) -> None:
        """Removes a track from the distribution."""
        
        if not isinstance(track, Track):
            raise TypeError("unsupported type for track: "
                            f"'{type(track).__name__}'")
        
        if track not in self.tracks:
            raise ValueError("'track' not in tracks")
        
        self.tracks.remove(track)
    
    def get_track(self, trackid: int) -> Track | None:
        """Returns the track of a track ID in the distribution."""
        
        trackids = [track.trackid for track in self.tracks]
        
        if trackid not in trackids:
            return 
        
        return self.tracks[trackids.index(trackid)]

class Slot(object):
    
    def __init__(self, cup: int, track: int, arena = False) -> None:
        if not isinstance(cup, int):
            raise TypeError("unsupported type for cup: "
                            f"'{type(cup).__name__}'")
        
        if not isinstance(track, int):
            raise TypeError("unsupported type for track: "
                            f"'{type(track).__name__}'")
        
        if track not in range(1, 5):
            raise ValueError("value of track must be 1, 2, 3 or 4")
        
        self.cup = cup
        self.track = track
        self.arena = arena
    
    def __repr__(self) -> str:
        """Represents the object in a console."""
        
        return str(self)
    
    def __str__(self) -> str:
        """Returns the cup and track with a dot."""
        
        string = f"{self.cup}.{self.track}"
        return f"A{string}" if self.arena else string
    
    def __add__(self, amount: int) -> tp.Self:
        """Adds an integer to a slot."""
        
        if not isinstance(amount, int):
            raise TypeError("unsupported type for amount: "
                            f"'{type(amount).__name__}'")
        
        if amount < 0:
            raise ValueError("value of amount must be non-negative")
        
        result = self
        maximum_per_cup = 5 if self.arena else 4
        for _ in range(amount):
            result.track += 1
            if result.track > maximum_per_cup:
                result.cup += 1
                result.track = 1
        
        return result
