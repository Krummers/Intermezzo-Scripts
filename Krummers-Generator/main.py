import script_utilities.functions as ft

import create
import folders as fd
import generate
import delete

import Modules.enumerables as eb

def main() -> None:
    fd.generate_folders()
    
    while True:
        actions = list(eb.Action)
        display = [action.name for action in actions]
        action = ft.options_question(actions,
                                     "What action needs to be performed?",
                                     display)
        
        match action.name:
            case "Create":
                create.main()
            case "Generate":
                generate.main()
            case "Delete":
                delete.main()
            case "Exit":
                return

if __name__ == "__main__":
    main()
