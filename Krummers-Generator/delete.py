import os
import script_utilities.file as fl
import script_utilities.functions as ft

import common as cm
import folders as fd

selections = fd.get_folder("Selections")

def main() -> None:
    folders = fd.get_selections()
    selection = cm.select_from_list(folders, "Which selection needs to be deleted?")
    
    confirmation = ft.question(f"Are you sure selection \"{selection}\" needs to be deleted?")
    if confirmation:
        selection = fl.Folder(os.path.join(selections.path, selection))
        selection.delete()

if __name__ == "__main__":
    main()
