import create
import folders as fd
import generate
import delete

import Modules.constants as cs

fd.generate_folders()

def print_menu(actions: list[str]) -> None:
    for x in range(len(actions)):
        print(chr(x + 65), ". ", actions[x].capitalize(), sep = "")

def select_action(actions: list[str]) -> str:
    while True:
        choice = input("What action needs to be performed? (Enter the corresponding option): ")
        
        if len(choice) != 1:
            print("This is not an option. Please try again.")
        elif ord(choice.upper()) - 65 in range(len(actions)):
            return actions[ord(choice.upper()) - 65]
        else:
            print("This is not an option. Please try again.")

def main() -> None:
    while True:
        actions = cs.actions
        print_menu(actions)
        action = select_action(actions)
        
        if action == "exit":
            return
        else:
            exec(f"{action}.main()")

if __name__ == "__main__":
    main()
