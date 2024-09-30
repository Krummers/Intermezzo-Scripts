import os

import Modules.file as fl

def get_folder(name: str) -> fl.Folder:
    cwd = os.getcwd()
    folder = fl.Folder(os.path.join(cwd, name))
    return folder

def get_selections() -> list[str]:
    selections = get_folder("Selections")
    folders = os.listdir(selections.path)
    return folders

def generate_folders() -> None:
    for folder in ["Selections", "Generations"]:
        folder = get_folder(folder)
        if not folder.exists():
            os.mkdir(folder.path)

def make_generation_folder(selection: str) -> fl.Folder:
    generations = get_folder("Generations")
    generation = fl.Folder(os.path.join(generations.path, selection))
    
    if generation.exists():
        generation.delete()
    
    os.mkdir(generation.path)
    
    return generation
