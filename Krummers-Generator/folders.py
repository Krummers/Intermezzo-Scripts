import os
import script_utilities.file as fl

def get_folder(name: str) -> fl.Folder:
    cwd = os.getcwd()
    folder = fl.Folder(os.path.join(cwd, name))
    return folder

def get_selections() -> list[str]:
    selections = get_folder("Selections")
    folders = os.listdir(selections.path)
    
    order = []
    
    for folder in folders:
        if folder.startswith("IM") and len(folder.split("-")) == 4:
            _, day, month, year = folder.split("-")
            sorting_attribute = (folder, f"IM-{year}-{month}-{day}")
        elif folder.startswith("IM") and len(folder.split("-")) == 3:
            _, week, year = folder.split("-")
            week = week[1:] if len(week) == 3 else f"0{week}"
            sorting_attribute = (folder, f"IM-{year}-{week}")
        else:
            sorting_attribute = (folder, folder)
        
        order.append(sorting_attribute)
    
    order = sorted(order, key = lambda x:x[1])
    sorted_folders = [folder[0] for folder in order]
    
    return sorted_folders

def generate_folders() -> None:
    for folder in ["Selections", "Generations"]:
        folder = get_folder(folder)
        if not bool(folder):
            os.mkdir(folder.path)

def make_generation_folder(selection: str) -> fl.Folder:
    generations = get_folder("Generations")
    generation = fl.Folder(os.path.join(generations.path, selection))
    
    if bool(generation):
        generation.delete()
    
    os.mkdir(generation.path)
    
    return generation
