import cloudscraper as cc
import json as js
import os
import platform as pf
import requests as rq

import Modules.constants as cs
import Modules.file as fl

cwd = os.getcwd()

def download(link, path, progress = None):
    with open(path, "wb") as file:
        with rq.get(link, stream = True) as data:
            if progress:
                print(f"Downloading {progress}...")
                total = data.headers.get("content-length")
                
                if total is None:
                    file.write(data.content)
                else:
                    size = os.get_terminal_size()[0] - 15
                    download = 0
                    total = int(total)
                    for chunk in data.iter_content(chunk_size = 1024):
                        download += len(chunk)
                        file.write(chunk)
                        percentage = int(100 * download / total)
                        completion = int(size * download / total)
                        print(f"\r[{'=' * completion}{' ' * (size - completion)}]", f"{percentage}%", end = "") 
                print("\n")
            else:
                file.write(data.content)

def question(string):
    while True:
        choice = str(input(string + " (Y or N): ")).lower()
        
        if choice in cs.binaries[:2]:
            return True
        elif choice in cs.binaries[2:]:
            return False
        else:
            print("This is not an option. Please try again.")

def drive_selection():
    if pf.uname()[0] == "Windows":
        drives = []
        for letter in [chr(x) for x in range(65, 65 + 26)]:
            if os.path.exists(f"{letter}:"):
                drives.append(letter)
        
        for letter in drives:
            print(f"{letter}. Drive {letter}:")
        
        while True:
            choice = str(input("Which drive should be used? (Enter the corresponding option): ")).upper()
            
            if choice in drives:
                return f"{choice}:"
            else:
                print("This is not an option. Please try again.")
    else:
        return os.path.splitdrive(cwd)[0]

def clear_screen():
    if pf.uname()[0] == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def get_translations():
    scraper = cc.create_scraper(browser = {"custom": "ScraperBot"})
    text = scraper.get("https://wiki.tockdom.com/info-w/translations.json").text
    json = js.loads(text)
    return json["translate"]

def get_prefixes():
    file = fl.TXT(os.path.join(os.getcwd(), "prefixes.txt"))
    download("https://ct.wiimm.de/export/prefix", file.path)
    
    info = file.read()
    
    prefixes = set()
    for k in range(len(info)):
        if info[k][0] == "#" or info[k][0] == "@":
            continue
        prefixes.add(info[k][:info[k].find("|")])
    file.delete()
    return prefixes

def rename_riivolution(riivolution, Wiimm_Intermezzo, new_suffix):
    for file in os.listdir(riivolution.path):
        if file.endswith(".xml"):
            xml = fl.TXT(os.path.join(riivolution.path, file))
            break
    if xml.filename != "Wiimm-Intermezzo.xml":
        current_suffix = xml.filename[len("Wiimm-Intermezzo-"):xml.filename.find(".xml")]
    else:
        current_suffix = ""
    lines = xml.read()
    for x in range(len(lines)):
        lines[x] = lines[x].replace(f"WiimmIntermezzo{current_suffix}", f"WiimmIntermezzo{new_suffix}")
        if current_suffix:
            lines[x] = lines[x].replace(f"Wiimm-Intermezzo-{current_suffix}", f"Wiimm-Intermezzo-{new_suffix}")
        else:
            lines[x] = lines[x].replace("Wiimm-Intermezzo", f"Wiimm-Intermezzo-{new_suffix}")
    xml.write(lines)
    xml.rename(f"Wiimm-Intermezzo-{new_suffix}.xml")
    Wiimm_Intermezzo.rename(f"Wiimm-Intermezzo-{new_suffix}")
    return riivolution, Wiimm_Intermezzo
